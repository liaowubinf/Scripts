# -*- coding: UTF-8 -*-
import os
import locale

import nuke
import nukescripts

import edit
import csheet
import asset
import pref

SYS_CODEC = locale.getdefaultlocale()[1]

def add_callback():
    def _cgtw():
        from . import cgtw
        def on_close_callback():
            if os.path.basename(nuke.scriptName()).startswith('SNJYW'):
                cgtw.Shot().upload_image()
        nuke.addOnScriptClose(on_close_callback)
    
    def _dropframe():
        _dropframe = asset.DropFrameCheck()
        nuke.addOnCreate(lambda : _dropframe.getDropFrameRanges(nuke.thisNode()), nodeClass='Read')
        nuke.addOnScriptSave(_dropframe.show)

    def _create_csheet():
        if nuke.numvalue('preferences.wlf_create_csheet', 0.0):
            csheet.create_csheet()

    def _check_project():
        if not nuke.value('root.project_directory'):
            nuke.message('工程目录未设置')

    def _lock_connections():
        if nuke.numvalue('preferences.wlf_lock_connections', 0.0):
            nuke.Root()['lock_connections'].setValue(1);
            nuke.Root().setModified(False)

    def _jump_frame():
        if nuke.numvalue('preferences.wlf_lock_connection', 0.0) and nuke.exists('_Write.knob.frame'):
            nuke.frame(nuke.numvalue('_Write.knob.frame'));
            nuke.Root().setModified(False)

    def _send_to_render_dir():
        if nuke.modified():
            return False
        
        if nuke.numvalue('preferences.wlf_send_to_dir', 0.0):
            asset.sent_to_dir(nuke.value('preferences.wlf_render_dir'))
    def _render_jpg():
        if nuke.modified():
            return False

        if nuke.numvalue('preferences.wlf_send_to_dir', 0.0):
            nuke.toNode('_Write')['bt_render_JPG'].execute()

    nuke.addBeforeRender(create_out_dirs, nodeClass='Write')
    if nuke.env['gui']:
        _dropframe()
        _cgtw()
        add_dropdata_callback()
        nuke.addOnScriptSave(edit.enableRSMB, kwargs={'prefix': '_'})
        nuke.addOnScriptSave(_check_project)
        nuke.addOnScriptSave(_lock_connections)
        nuke.addOnScriptSave(_jump_frame)
        nuke.addOnScriptClose(_render_jpg)
        nuke.addOnScriptClose(_create_csheet)
        nuke.addOnScriptClose(_send_to_render_dir)

def create_out_dirs():
    trgDir = os.path.dirname( nuke.filename( nuke.thisNode() ) )
    if not os.path.isdir( trgDir ):
        os.makedirs( trgDir )

def add_dropdata_callback():
    def _db(type, data):
        if type == 'text/plain' and os.path.basename(data).lower() == 'thumbs.db':
            return True
        else:
            return None

    def _fbx(type, data):
        if type == 'text/plain' and data.endswith('.fbx'):
            camera_node = nuke.createNode('Camera2', 'read_from_file True file {data} frame_rate 25 suppress_dialog True label {{导入的摄像机：\n[basename [value file]]\n注意选择file -> node name}}'.format(data=data))
            camera_node.setName('Camera_3DEnv_1')
            return True
        else:
            return None

    def _vf(type, data):
        if type == 'text/plain' and data.endswith('.vf'):
            vectorfield_node = nuke.createNode('Vectorfield', 'vfield_file "{data}" file_type vf label {{[value this.vfield_file]}}'.format(data=data))
            return True
        else:
            return None
            
    def _else(type, data):
        if type == 'text/plain':
            nuke.createNode('Read', 'file "{}"'.format(data))
            return True
        else:
            return None
            
    def _dir(type, data):
        def _file(type, data):
            _db(type, data)
            _fbx(type, data)
            _vf(type, data)
            _else(type, data)
            
        def _path(type, data):
            if os.path.isdir(data):
                _dir(type, data)
                return True
            else:
                _file(type, data)
                return True

        if type == 'text/plain' and os.path.isdir(data):
            _dir = data.replace('\\', '/')
            for i in nuke.getFileNameList(_dir):
                _path(type, '/'.join([_dir, i]))
            return True
        else:
            return None

    nuke.addOnCreate(lambda : edit.randomGlColor(nuke.thisNode()))

    nukescripts.addDropDataCallback(_fbx)
    nukescripts.addDropDataCallback(_vf)
    nukescripts.addDropDataCallback(_db)
    nukescripts.addDropDataCallback(_dir)
    
    def _catch_all(type, data):
        print(type)
        print(data)
        return None
        
    # nukescripts.addDropDataCallback(_catch_all)
    # nuke.addOnScriptLoad(SNJYW.setProjectRoot)
    # nuke.addOnScriptLoad(SNJYW.setRootFormat)