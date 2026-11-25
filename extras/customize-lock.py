#!/usr/bin/env python3
"""Restyle a user-owned clone of Omarchy's lock view for the Omarchy Nigeria theme.

Visual changes only. Authentication (Service.qml, the password field's
behaviour, failure and fingerprint handling) is left exactly as Omarchy ships
it. Every change is keyed off the active theme: when the current theme ships a
`lock-emblem.svg`, the lock shows

  * the wallpaper itself, sharp, under a light green wash, instead of a heavy blur;
  * the omarchy.org hero set straight into the photo over a soft centre shade
    (`lock-glow.svg`): the theme's pixel wordmark with an "NG" edition badge, and
    a compact password field styled like the site's buttons, with a scattered
    pixel field (`lock-pixels.svg`) over the edges of the photo;
  * a "Place · photo by Name" credit, read from wallpaper files named
    `NN-place-by-photographer.ext`.

Any other theme gets Omarchy's stock lock screen unchanged.

Usage: customize-lock.py <path-to-cloned-lock-plugin>
"""
from pathlib import Path
import sys

MARKER = "// Nigeria theme lock styling"


def replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise SystemExit(
            f"Unsupported lock view layout: expected one match for {old.strip()[:60]!r}. "
            "Omarchy's lock view has probably changed; re-clone it and update this script."
        )
    return source.replace(old, new, 1)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    view = Path(sys.argv[1]) / "LockView.qml"
    s = view.read_text()
    if MARKER in s:
        print("Nigeria lock styling is already installed")
        return

    s = replace_once(s, "import qs.Ui\n", "import qs.Ui\nimport Quickshell\nimport Quickshell.Io\n")

    # Scale the dialog up on large displays so it is not lost on a 5K monitor.
    s = replace_once(s, "  readonly property int fieldWidth: 381\n", "  readonly property int fieldWidth: root.themedLock ? Math.round(root.emblemWidth * 0.227) : 381\n")
    s = replace_once(s, "  readonly property int fieldHeight: 67\n", "  readonly property int fieldHeight: root.themedLock ? Math.round(root.emblemWidth * 0.0445) : 67\n")

    s = replace_once(
        s,
        "  readonly property bool video: Util.isVideoPath(root.backgroundPath)\n",
        "  readonly property bool video: Util.isVideoPath(root.backgroundPath)\n"
        "\n"
        f"  {MARKER}: on only while the current theme ships lock-emblem.svg.\n"
        '  readonly property string themeDir: (Quickshell.env("XDG_STATE_HOME") || (Quickshell.env("HOME") + "/.local/state")) + "/omarchy/current/theme"\n'
        "  readonly property bool themedLock: themeEmblem.status === Image.Ready\n"
        "  readonly property real uiScale: root.themedLock ? Math.max(1, Math.min(1.6, root.width / 2560)) : 1\n"
        "  readonly property int cardPadding: Math.round(44 * root.uiScale)\n"
        "  readonly property int emblemWidth: Math.round(Math.min(root.width * 0.40, root.height * 1.6))\n"
        "  readonly property int emblemHeight: Math.round(root.emblemWidth * 285 / 1215)\n"
        "  readonly property int captionGap: Math.round(22 * root.uiScale)\n"
        "  readonly property int captionHeight: Math.round(Math.max(24 * root.uiScale, root.emblemWidth * 0.028))\n"
        "  readonly property int fieldGap: Math.round(34 * root.uiScale)\n"
        "  readonly property int cardWidth: root.emblemWidth + root.cardPadding * 2\n"
        "  readonly property int cardHeight: root.cardPadding * 2 + root.emblemHeight + root.captionGap + root.captionHeight + root.fieldGap + root.fieldHeight\n"
        "  // Credit from the theme's credits.json; else from NN-place-by-photographer.ext.\n"
        "  property var themeCredits: ({})\n"
        "  onBackgroundPathChanged: if (root.themedLock) lockCredits.reload()\n"
        "  readonly property string photoCredit: {\n"
        '    var file = String(root.backgroundPath).split("/").pop()\n'
        '    var c = Object.prototype.hasOwnProperty.call(root.themeCredits, file) ? root.themeCredits[file] : null\n'
        '    if (c && typeof c.place === "string" && typeof c.photographer === "string" && c.place.length > 0 && c.photographer.length > 0)\n'
        '      return c.place.slice(0, 80) + "  ·  photo by " + c.photographer.slice(0, 60)\n'
        '    var name = file.replace(/\\.[^.]+$/, "").replace(/^\\d+-/, "")\n'
        '    var split = name.lastIndexOf("-by-")\n'
        '    if (split <= 0) return ""\n'
        '    var words = function(text) { return text.split("-").filter(function(w) { return w.length > 0 }).map(function(w) { return w.charAt(0).toUpperCase() + w.slice(1) }).join(" ") }\n'
        '    return words(name.slice(0, split)) + "  ·  photo by " + words(name.slice(split + 4))\n'
        "  }\n",
    )

    # Show the photograph itself rather than an unrecognisable blur.
    s = replace_once(s, "      blur: 1.0\n", "      blur: root.themedLock ? 0.0 : 1.0\n")
    s = replace_once(
        s,
        "      contrast: -0.08\n",
        "      contrast: root.themedLock ? 0.04 : -0.08\n"
        "      // Nigeria: grade the photo toward the theme's greens so it and the wordmark share a palette.\n"
        "      saturation: root.themedLock ? -0.25 : 0.0\n"
        "      brightness: root.themedLock ? -0.10 : 0.0\n"
        "      colorization: root.themedLock ? 0.22 : 0.0\n"
        '      colorizationColor: "#1A3A2A"\n',
    )

    s = replace_once(
        s,
        "    MouseArea {\n      anchors.fill: parent\n      hoverEnabled: true\n",
        f"""    {MARKER}: wash, card, emblem and credit sit between wallpaper and input.
    Rectangle {{
      anchors.fill: parent
      visible: root.themedLock
      gradient: Gradient {{
        GradientStop {{ position: 0.0; color: Qt.rgba(0.06, 0.10, 0.08, 0.10) }}
        GradientStop {{ position: 0.6; color: Qt.rgba(0.06, 0.10, 0.08, 0.28) }}
        GradientStop {{ position: 1.0; color: Qt.rgba(0.06, 0.10, 0.08, 0.55) }}
      }}
    }}

    Image {{
      anchors.fill: parent
      visible: root.themedLock
      source: root.themedLock ? "file://" + root.themeDir + "/lock-pixels.svg" : ""
      sourceSize.height: parent.height
      fillMode: Image.PreserveAspectCrop
      smooth: false
      cache: false
      opacity: 0.75
    }}

    FileView {{
      id: lockCredits
      path: root.themeDir + "/credits.json"
      watchChanges: true
      onFileChanged: reload()
      onLoaded: {{
        try {{
          var t = String(text() || "")
          var d = t.length > 0 && t.length < 200000 ? JSON.parse(t) : null
          root.themeCredits = d && typeof d === "object" && !Array.isArray(d) ? d : ({{}})
        }} catch (e) {{ root.themeCredits = ({{}}) }}
      }}
      onLoadFailed: root.themeCredits = ({{}})
    }}

    // Twinkles, as on omarchy.org: small checkerboard clusters that light up
    // near the edges and fade away. Static when animations are turned off.
    Repeater {{
      model: root.themedLock && Style.duration(1000) > 0 ? 8 : 0

      delegate: Item {{
        id: spark
        readonly property real cell: 14 * Math.max(root.width / 2560, root.height / 1080)
        readonly property var tints: ["#39D98A", "#8CE3B4", "#F5FFF9", "#5BCD93"]
        property color tint: "#39D98A"
        width: cell * 5
        height: cell * 5
        opacity: 0

        function relocate() {{
          var cols = Math.max(1, Math.floor(root.width / cell) - 5)
          var rows = Math.max(1, Math.floor(root.height / cell) - 5)
          for (var tries = 0; tries < 20; tries++) {{
            var cx = Math.floor(Math.random() * cols), cy = Math.floor(Math.random() * rows)
            var fx = (cx + 2.5) / (cols + 5), fy = (cy + 2.5) / (rows + 5)
            // Keep the middle clear for the wordmark and field.
            if (Math.abs(fx - 0.5) < 0.28 && Math.abs(fy - 0.5) < 0.30) continue
            x = cx * cell
            y = cy * cell
            break
          }}
          tint = tints[Math.floor(Math.random() * tints.length)]
        }}

        Repeater {{
          model: 25
          Rectangle {{
            readonly property int r: Math.floor(index / 5)
            readonly property int c: index % 5
            visible: Math.abs(r - 2) + Math.abs(c - 2) <= 2 && (r + c) % 2 === 0
            x: c * spark.cell + 2
            y: r * spark.cell + 2
            width: spark.cell - 4
            height: spark.cell - 4
            color: spark.tint
            opacity: r === 2 && c === 2 ? 1.0 : 0.75
          }}
        }}

        // One twinkle: fade in, hold, fade out. The timer starts the next one.
        SequentialAnimation {{
          id: twinkle
          NumberAnimation {{ target: spark; property: "opacity"; from: 0; to: 0.9; duration: Style.duration(260); easing.type: Easing.OutCubic }}
          PauseAnimation {{ duration: 700 }}
          NumberAnimation {{ target: spark; property: "opacity"; to: 0; duration: Style.duration(900); easing.type: Easing.OutCubic }}
        }}

        Timer {{
          id: nextTwinkle
          running: root.themedLock && root.visible
          repeat: false
          interval: 300 + Math.floor(Math.random() * 3000)
          onTriggered: {{
            if (!twinkle.running) {{
              spark.relocate()
              twinkle.start()
            }}
            interval = 2200 + Math.floor(Math.random() * 4800)
            restart()
          }}
        }}
      }}
    }}

    Image {{
      anchors.centerIn: parent
      width: root.cardWidth * 2.4
      height: root.cardHeight * 2.6
      visible: root.themedLock
      source: root.themedLock ? "file://" + root.themeDir + "/lock-glow.svg" : ""
      sourceSize.width: 800
      fillMode: Image.Stretch
      cache: false
    }}

    Rectangle {{
      id: nigeriaCard
      visible: root.themedLock
      anchors.centerIn: parent
      width: root.cardWidth
      height: root.cardHeight
      // Layout anchor only: the wordmark sits directly in the photo, as on omarchy.org.
      color: "transparent"
    }}

    Image {{
      id: themeEmblem
      anchors.top: nigeriaCard.top
      anchors.topMargin: root.cardPadding
      anchors.horizontalCenter: nigeriaCard.horizontalCenter
      width: root.emblemWidth
      height: root.emblemHeight
      visible: root.themedLock
      source: "file://" + root.themeDir + "/lock-emblem.svg"
      sourceSize.width: root.emblemWidth * 2
      fillMode: Image.PreserveAspectFit
      smooth: false
      cache: false
      asynchronous: false
      layer.enabled: root.themedLock
      layer.effect: MultiEffect {{
        shadowEnabled: true
        shadowColor: "#0F1A15"
        shadowOpacity: 0.85
        shadowBlur: 0.9
        shadowVerticalOffset: Math.round(4 * root.uiScale)
      }}
    }}

    // "NG" edition badge tucked under the wordmark's right edge.
    Rectangle {{
      visible: root.themedLock
      anchors.top: themeEmblem.bottom
      anchors.topMargin: root.captionGap
      anchors.right: themeEmblem.right
      width: ngText.implicitWidth + Math.round(root.captionHeight * 0.7)
      height: root.captionHeight
      color: Qt.rgba(0.22, 0.85, 0.54, 0.12)
      border.width: 1
      border.color: Qt.rgba(0.22, 0.85, 0.54, 0.6)

      Text {{
        id: ngText
        textFormat: Text.PlainText
        anchors.centerIn: parent
        text: "NG"
        color: Qt.rgba(0.66, 0.94, 0.78, 1.0)
        font.family: Style.font.family
        font.pixelSize: Math.round(Math.max(15 * root.uiScale, root.emblemWidth * 0.016))
        font.bold: true
        font.letterSpacing: Math.round(2 * root.uiScale)
      }}
    }}

    Rectangle {{
      visible: root.themedLock && root.photoCredit.length > 0
      anchors.left: parent.left
      anchors.bottom: parent.bottom
      anchors.margins: Math.round(32 * root.uiScale)
      width: creditText.implicitWidth + Math.round(36 * root.uiScale)
      height: creditText.implicitHeight + Math.round(18 * root.uiScale)
      radius: height / 2
      color: Qt.rgba(0.06, 0.10, 0.08, 0.72)

      Text {{
        id: creditText
        textFormat: Text.PlainText
        anchors.centerIn: parent
        text: root.photoCredit
        color: Qt.rgba(0.86, 0.91, 0.87, 1.0)
        font.family: Style.font.family
        font.pixelSize: Math.round(17 * root.uiScale)
      }}
    }}

    MouseArea {{
      anchors.fill: parent
      hoverEnabled: true
""",
    )

    # Seat the password field at the bottom of the card.
    s = replace_once(
        s,
        "      anchors.centerIn: parent\n      color: Commons.Color.lock.background\n",
        "      anchors.centerIn: parent\n"
        "      anchors.verticalCenterOffset: root.themedLock ? Math.round(root.cardHeight / 2 - root.cardPadding - root.fieldHeight / 2) : 0\n"
        "      color: Commons.Color.lock.background\n",
    )

    # Password field: the omarchy.org "See it in action" button, at the site's exact
    # ratio to the wordmark (204 x 40 to a 898px wordmark), square corners.
    # Text sized to the button's 15px label at the site's wordmark width.
    s = replace_once(
        s,
        "  readonly property int fieldFontSize: Math.round(Style.font.heading * 1.125)\n",
        "  readonly property int fieldFontSize: root.themedLock ? Math.round(root.emblemWidth * 0.0167) : Math.round(Style.font.heading * 1.125)\n",
    )
    s = replace_once(
        s,
        "  readonly property int passwordDotFontSize: Math.round(Style.font.heading * 1.33)\n",
        "  readonly property int passwordDotFontSize: root.themedLock ? Math.round(root.emblemWidth * 0.0167) : Math.round(Style.font.heading * 1.33)\n",
    )
    s = replace_once(s, "  readonly property int outlineThickness: 3\n", "  readonly property int outlineThickness: root.themedLock ? 1 : 3\n")
    s = replace_once(
        s,
        "      color: Commons.Color.lock.background\n      borderSpec: root.inputBorderSpec\n      radius: Style.cornerRadius\n",
        "      color: root.themedLock ? Qt.rgba(0.15, 0.22, 0.19, 0.95) : Commons.Color.lock.background\n"
        "      borderSpec: root.inputBorderSpec\n"
        "      radius: root.themedLock ? 0 : Style.cornerRadius\n",
    )

    view.write_text(s)
    print(f"Nigeria lock styling installed in {view}")


if __name__ == "__main__":
    main()
