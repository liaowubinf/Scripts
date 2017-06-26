# -*- coding=UTF-8 -*-
import nuke
import nukescripts

def set_knob_default():
    def _vectorblur2():
        nuke.knobDefault("VectorBlur2.uv", "motion")
        nuke.knobDefault("VectorBlur2.blur_uv", "uniform")
        nuke.knobDefault("VectorBlur2.uv_offset", "-0.5")
        nuke.knobDefault("VectorBlur2.scale", "30")
        nuke.knobDefault("VectorBlur2.soft_lines", "True")
        nuke.knobDefault("VectorBlur2.normalize", "True")

    def _root():
        nuke.knobDefault("Root.fps", "25")
        nuke.knobDefault("Root.format", "1920 1080 0 0 1920 1080 1 HD_1080")
        nuke.knobDefault("Root.project_directory", "[python {nuke.script_directory()}]")
        # nuke.knobDefault("Root.free_type_font_path", "//SERVER/scripts/NukePlugins/Fonts")

    def _zdefocus2():
        nuke.knobDefault("ZDefocus2.blur_dof", "0")
        nuke.knobDefault("ZDefocus2.math", "depth")

    _root()
    _vectorblur2()
    _zdefocus2()
    nuke.knobDefault("LayerContactSheet.showLayerNames", "1")
    nuke.knobDefault("note_font", u"微软雅黑".encode('utf8'))
    nuke.knobDefault("Switch.which", "1")
    nuke.knobDefault("Viewer.input_process", "False")
    nuke.knobDefault("SoftClip.conversion", "3")

def add_preferences():
    p = nuke.toNode('preferences')
    k = nuke.Tab_Knob('wlf_tab', '吾立方')
    p.addKnob(k)
    def _add_knob(k):
        _knob_tcl_name = 'preferences.{}'.format(k.name())
        if nuke.exists(_knob_tcl_name):
            k.setValue(p[k.name()].value())
            p.removeKnob(p[k.name()])
        k.setFlag(nuke.ALWAYS_SAVE)
        p.addKnob(k)

    k = nuke.Text_Knob('wlf_on_script_save', '保存时')
    _add_knob(k)

    k = nuke.Boolean_Knob('wlf_lock_connections', '锁定节点连接')
    k.setFlag(nuke.STARTLINE)
    _add_knob(k)

    k = nuke.Boolean_Knob('wlf_jump_frame', '跳至_Write节点指定的帧')
    k.setFlag(nuke.STARTLINE)
    _add_knob(k)

    k = nuke.Boolean_Knob('wlf_render_jpg', '渲染_Write节点单帧')
    k.setFlag(nuke.STARTLINE)
    _add_knob(k)

    k = nuke.Text_Knob('wlf_on_script_close', '保存并退出时')
    _add_knob(k)

    k = nuke.Boolean_Knob('wlf_send_to_dir', '发送至渲染文件夹')
    k.setFlag(nuke.STARTLINE)
    _add_knob(k)

    k = nuke.File_Knob('wlf_render_dir', '')
    k.clearFlag(nuke.STARTLINE)
    _add_knob(k)

    k = nuke.Boolean_Knob('wlf_create_csheet', '生成色板')
    k.setFlag(nuke.STARTLINE)
    _add_knob(k)

    def _remove_old():
        try:
            p.removeKnob(p['wlf_lock_connection'])
            p.removeKnob(p['wlf_tab'])
        except NameError:
            pass

    _remove_old()