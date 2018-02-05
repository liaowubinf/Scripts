import QtQuick 1.0

Rectangle {
    id: rect
 
    Component.onCompleted: {
        autoclose_timer.interval = 3000 + text.width * 20;
        text.width = Math.min(text.width, 300);
        autoclose_timer.start();
    }
 
    height: text.height + 50
    width: text.width + 50
    radius: 10
    color: "#b1bccd"
    border {
        width: 2
        color: "#dae2fe"
    }
    Timer {
        id: autoclose_timer
        onTriggered: disapear.start()
    }
    MouseArea {
        z: 0
        id: mousearea
        hoverEnabled: true
        onEntered: {
            autoclose_timer.stop();
            disapear.stop();
            rect.opacity = 1;
        }
        onExited:autoclose_timer.restart()
        anchors.fill: parent

    }
    Text {
        id: text
        color: "#0e0c0a"
        opacity: 0
        font{
            family: "微软雅黑,SimHei"
            pointSize: 15
        }
        text: DATA.text
        wrapMode: Text.Wrap
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        anchors.centerIn: parent
    }
    Rectangle{
        id: close_button
        height: 20
        width: 20
        radius: 8
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 10
        color: "transparent"
        Text {
            id: close_text
            text: "×"
            color: "grey"
            font.pointSize: 15
            anchors.centerIn: parent
        }
        MouseArea{
            acceptedButtons: Qt.LeftButton
            anchors.fill: close_button
            onClicked: VIEW.close()
            hoverEnabled: true
            onEntered: {
                parent.color = "#e81123"
                close_text.color = "white"
            }
            onExited: {
                parent.color = "transparent"
                close_text.color = "grey"
            }
        }
    }

    ParallelAnimation {
        running:true
        NumberAnimation {
            target: rect;
            property: "opacity"
            from: 0; to: 1
            duration: 200 
        }
        NumberAnimation {
            target: rect;
            property: "x"
            from: 200; to: 0
            duration: 200
        }
        NumberAnimation {
            target: text;
            property: "opacity"
            from: 0; to: 1
            duration: 300
        }
    }
    SequentialAnimation {
        id: disapear
        NumberAnimation { target: rect; property: "opacity"; to: 0; duration: 500 }
        ScriptAction { script: { mousearea.enabled = false; }
        }
        NumberAnimation { target: VIEW; property: "height_"; to: 0; duration: 500 }
        ScriptAction { script: VIEW.close(); }
    }
}