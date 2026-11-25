import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import QtQuick
import qs.Commons
import qs.Commons as Commons

// Photo credit for the desktop: a small pill in the bottom-left corner of every
// screen, below all windows, naming the place and photographer of the current
// wallpaper. Clicking it opens the photographer's profile.
//
// Credits come from `credits.json` in the active theme, keyed by wallpaper
// filename: { "file.jpg": { "place": ..., "photographer": ..., "profile": "https://..." } }.
// Themes without that file show nothing.
Item {
  id: root

  property var shell: null
  property bool suspended: false

  readonly property string stateHome: Quickshell.env("XDG_STATE_HOME") || (Quickshell.env("HOME") + "/.local/state")
  readonly property string backgroundLink: stateHome + "/omarchy/current/background"
  readonly property string creditsPath: stateHome + "/omarchy/current/theme/credits.json"

  property string backgroundPath: ""
  property var credits: ({})

  readonly property string fileName: String(backgroundPath).split("/").pop()
  readonly property var entry: {
    var e = Object.prototype.hasOwnProperty.call(credits, fileName) ? credits[fileName] : null
    return Util.isPlainObject(e) ? e : null
  }
  // Credits are file data: plain text only, bounded, and only https links open.
  function field(name, limit) {
    var value = entry ? entry[name] : ""
    return typeof value === "string" ? value.replace(/[\r\n\t]+/g, " ").trim().slice(0, limit) : ""
  }
  readonly property string place: field("place", 80)
  readonly property string photographer: field("photographer", 60)
  readonly property string profile: {
    var url = field("profile", 300)
    return /^https:\/\/[A-Za-z0-9.-]+\/[^\s"'<>]*$/.test(url) ? url : ""
  }
  readonly property bool hasCredit: place.length > 0 && photographer.length > 0

  function parseCredits() {
    var text = String(creditsFile.text() || "")
    if (text.length === 0 || text.length > 200000) { credits = ({}); return }
    try {
      var data = JSON.parse(text)
      credits = Util.isPlainObject(data) ? data : ({})
    } catch (e) {
      credits = ({})
    }
  }

  FileView {
    id: creditsFile
    path: root.creditsPath
    watchChanges: true
    onFileChanged: reload()
    onLoaded: root.parseCredits()
    onLoadFailed: root.credits = ({})
  }

  // The background symlink is repointed on every change; poll it cheaply.
  Process {
    id: readlinkProc
    command: ["readlink", "-f", "--", root.backgroundLink]
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: {
        var next = String(text || "").trim()
        if (next !== root.backgroundPath) {
          root.backgroundPath = next
          creditsFile.reload()
        }
      }
    }
  }

  Timer {
    interval: 2000
    running: !root.suspended
    repeat: true
    triggeredOnStart: true
    onTriggered: if (!readlinkProc.running) readlinkProc.running = true
  }

  Variants {
    model: Quickshell.screens

    PanelWindow {
      required property var modelData
      screen: modelData
      visible: root.hasCredit && !root.suspended
      color: "transparent"
      anchors { bottom: true; left: true }
      margins { bottom: 24; left: 24 }
      implicitWidth: pill.width
      implicitHeight: pill.height
      exclusionMode: ExclusionMode.Ignore
      WlrLayershell.namespace: "nigeria-photo-credit"
      WlrLayershell.layer: WlrLayer.Bottom
      WlrLayershell.keyboardFocus: WlrKeyboardFocus.None

      Rectangle {
        id: pill
        width: row.implicitWidth + 28
        height: row.implicitHeight + 14
        radius: height / 2
        color: Qt.rgba(0.06, 0.10, 0.08, mouse.containsMouse ? 0.92 : 0.72)
        border.width: 1
        border.color: mouse.containsMouse && root.profile.length > 0 ? Qt.rgba(0.22, 0.85, 0.54, 0.8) : Qt.rgba(0.96, 1.0, 0.98, 0.12)
        Behavior on color { ColorAnimation { duration: Style.duration(150) } }

        Row {
          id: row
          anchors.centerIn: parent
          spacing: 10

          Text {
            textFormat: Text.PlainText
            text: root.place
            color: Qt.rgba(0.86, 0.91, 0.87, 1.0)
            font.family: Style.font.family
            font.pixelSize: 15
          }
          Text {
            textFormat: Text.PlainText
            text: "·"
            color: Qt.rgba(0.49, 0.60, 0.55, 1.0)
            font.family: Style.font.family
            font.pixelSize: 15
          }
          Text {
            textFormat: Text.PlainText
            text: "photo by " + root.photographer + (root.profile.length > 0 ? "  ↗" : "")
            color: mouse.containsMouse && root.profile.length > 0 ? "#39D98A" : Qt.rgba(0.71, 0.79, 0.74, 1.0)
            font.family: Style.font.family
            font.pixelSize: 15
          }
        }

        MouseArea {
          id: mouse
          anchors.fill: parent
          hoverEnabled: true
          cursorShape: root.profile.length > 0 ? Qt.PointingHandCursor : Qt.ArrowCursor
          onClicked: if (root.profile.length > 0) Util.execArgv(["xdg-open", root.profile])
        }
      }
    }
  }
}
