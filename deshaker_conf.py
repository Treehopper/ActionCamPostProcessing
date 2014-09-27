"""
Usage: deshaker_conf.py [--deshaker=N [--ds-motion-smoothness=H,V,R,Z] [--ds-zoom-factor=X] [--ds-edge-compensation=C] [--ds-rolling-shutter=S]] [--convert-fps=F] [--smoother] [--vcompress] [--acompress]
       deshaker_conf.py (-h | --help)

Options:
    -h, --help
    --deshaker=N  Include deshaker configuration in pass 1 or 2
    --smoother  Include smoother configuration
	--convert-fps=F Set target framerate to F
	--ds-edge-compensation=C C is a value between 0 and 4: 0:None (large borders), 1:Adaptive zoom average (some borders), 2:Adaptive zoom full (no borders), 3:Fixed zoom (no borders), 4:Adaptive zoom average + fixed zoom (no borders)

Examples:
    deshaker_conf.py --deshaker=1
    deshaker_conf.py --deshaker=2 --ds-motion-smoothness=100,100,100,100 --ds-zoom-factor=1.1 --ds-edge-compensation=3 --ds-rolling-shutter=88.89 --convert-fps=30 --acompress --vcompress --smoother
"""

# Docopt is a library for parsing command line arguments
import docopt
import subprocess
import os

pass2_conf = """\
VirtualDub.audio.SetSource(1);
VirtualDub.audio.SetInterleave(1,500,1,0,0);
VirtualDub.audio.SetClipMode(1,1);
VirtualDub.audio.SetEditMode(1);
VirtualDub.audio.SetConversion(0,0,0,0,0);
VirtualDub.audio.SetVolume();
VirtualDub.audio.EnableFilterGraph(0);
VirtualDub.video.SetInputFormat(0);
VirtualDub.video.SetOutputFormat(0);
VirtualDub.video.SetMode(3);
VirtualDub.video.SetSmartRendering(0);
VirtualDub.video.SetPreserveEmptyFrames(0);
VirtualDub.video.SetFrameRate2(0,0,1);
VirtualDub.video.SetIVTC(0, 0, 0, 0);
"""

vcompress_on = """\
VirtualDub.video.SetCompression(0x64697678,0,10000,0);
VirtualDub.video.SetCompData(3540,"AAAAALwCAACQsggALlx2aWRlby5wYXNzAAAAAHN0YXRzAAAAcXVhbGl0eQBwcm9maWxlAG51bV90aHJlYWRzAGNwdV9mbGFncwAAAGRpc3BsYXlfc3RhdHVzAAB2b3BfZGVidWcAAABkZWJ1ZwAAAGZvdXJjY191c2VkAHRyZWxsaXNfcXVhbnQAAABtYXhfYnF1YW50AABtaW5fYnF1YW50AABtYXhfcHF1YW50AABtaW5fcHF1YW50AABtYXhfaXF1YW50AABtaW5faXF1YW50AABmcmFtZV9kcm9wX3JhdGlvAAAAAG1heF9rZXlfaW50ZXJ2YWwAAAAAdHVyYm8AAABjaHJvbWFtZQAAAAAAAAAAkAEAAFh2aWQgSG9tZQAAAFh2aWQgTW9iaWxlAAEAAAABAAAADAAAAAsAAAAKAAAACwAAABAAAAALAAAAKAAAACEAAAAAAAAAAAAAAPSL3QL0i90CAAAAAGABAADwAAAAHgAAAAEAAADeAwAASgEAAKwmAABkAAAAAAAQAP////9CXhQAABJ6AAUAAADXAgAA6IvdAuiL3QIAAAAA0AIAAEACAAAZAAAAAQAAAPwSAABUBgAANJ4AAGQAAAAAADAA//////AQSgAAEnoABQAAAN8CAADci90C3IvdAgAAAAAABQAA0AIAAB4AAAABAAAAMCoAABAOAADgpQEAZAAAAAAAYAD/////AQAAAEdlbmVyYWwgcHVycG9zZQBSZWFsLXRpbWUAAAAodW5yZXN0cmljdGVkKQAATVBFRzQgQVNQIEAgTDUAAE1QRUc0IEFkdmFuY2VkIFNpbXBsZSBAIEw1AABNUEVHNCBBU1AgQCBMNAAATVBFRzQgQWR2YW5jZWQgU2ltcGxlIEAgTDQAAE1QRUc0IEFTUCBAIEwzAABNUEVHNCBBZHZhbmNlZCBTaW1wbGUgQCBMMwAATVBFRzQgQVNQIEAgTDIAAE1QRUc0IEFkdmFuY2VkIFNpbXBsZSBAIEwyAABNUEVHNCBBU1AgQCBMMQAATVBFRzQgQWR2YW5jZWQgU2ltcGxlIEAgAQAAAAAAAAAIERITFRcZGxESExUXGRscFBUWFxgaHB4VFhcYGhweIBYXGBocHiAjFxgaHB4gIyYZGhweICMmKRscHiAjJiktEBESExQVFhcREhMUFRYXGBITFBUWFxgZExQVFhcYGhsUFRYXGRobHBUWFxgaGxweFhcYGhscHh8XGBkbHB4fIQAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAIAAACWAAAAZAAAAAEAAAAAAAAABAAAAAMAAAABAAAAAQAAAAAAAAABAAAAAAAAAAAAAAAAAAAAZAAAAPQBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAABkAAAAZAAAAAEAAAAKAAAAAQAAABQAAAAAAAAAAAAAAAUAAAAFAAAABQAAAAAoCgAAAAAAAQAAAAEAAAAeAAAAAAAAAAIAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAYAAAABAAAAAAAAAAAAAAABAAAAAAAAACwBAAAAAAAAAQAAAB8AAAABAAAAHwAAAAEAAAAfAAAAAQAAAAQAAAAAAAAAAAAAAAAAAAABAAAAAAAAAM8DAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAA");
"""

vcompress_off = """\
VirtualDub.video.SetCompression();
"""

acompress_on = """\
VirtualDub.audio.SetMode(1);
VirtualDub.audio.SetCompressionWithHint(85,32000,2,0,16000,1,12,"AQACAAAAQAIBAAAA","MPEG Layer-3 Codec");
"""

acompress_off = """\
VirtualDub.audio.SetMode(0);
VirtualDub.video.SetCompression();
"""

filters_begin = """\
VirtualDub.audio.filters.Clear();
"""

filters_end = filters_begin

deshaker_cfg = """\
VirtualDub.video.filters.Add("Deshaker v3.0");
VirtualDub.video.filters.instance[{filters_count}].Config("18|{pass_nr}|30|4|1|0|1|0|640|480|1|2|{ms_h}|{ms_v}|{ms_r}|{ms_z}|4|1|{edge_compensation}|2|8|30|300|4|Deshaker.log|0|0|0|0|0|0|0|0|0|0|0|0|0|{zoom_factor}|15|15|5|15|0|0|30|30|0|0|{rolling_shutter_on}|0|1|0|0|10|1000|1|{rolling_shutter}|1|1|20|5000|100|20|1");
"""

smoother_cfg = """\
VirtualDub.video.filters.Add("smoother");
VirtualDub.video.filters.instance[{filters_count}].Config(2000,0);
"""

convert_fps_cfg = """\
VirtualDub.video.SetTargetFrameRate({convert_fps_target},{convert_fps_factor});
"""

if __name__ == '__main__':
    try:
        # Parse arguments, use file docstring as a parameter definition
        arguments = docopt.docopt(__doc__)

        vcompress = arguments['--vcompress']
        if(vcompress):
            pass2_conf += vcompress_on
        else:
            pass2_conf += vcompress_off

        acompress = arguments['--acompress']
        if(acompress):
            pass2_conf += acompress_on
        else:
            pass2_conf += acompress_off


        # filters
        smoother = arguments['--smoother']




        pass_nr = arguments['--deshaker']
        if(not pass_nr is None):
            pass_nr = int(pass_nr)

        motion_smoothness = arguments['--ds-motion-smoothness']
        if(not motion_smoothness is None):
            motion_smoothness = arguments['--ds-motion-smoothness'].split(",")
            if(len(motion_smoothness) != 4):
                raise Exception("Supply all four motion smoothness values")
            ms_h = motion_smoothness[0]
            ms_v = motion_smoothness[1]
            ms_r = motion_smoothness[2]
            ms_z = motion_smoothness[3]

        zoom_factor = arguments['--ds-zoom-factor']
        if(not zoom_factor is None):
            zoom_factor = float(zoom_factor)

        convert_fps_factor=10000
        convert_fps = arguments['--convert-fps']
        if(not convert_fps is None):
            convert_fps_target = convert_fps_factor * int(convert_fps)
            pass2_conf += convert_fps_cfg.format(convert_fps_target=convert_fps_target, convert_fps_factor=convert_fps_factor)

        rolling_shutter_on = 0
        rolling_shutter = arguments['--ds-rolling-shutter']
        if(not rolling_shutter is None):
            rolling_shutter = float(rolling_shutter)
            rolling_shutter_on = 1

        edge_compensation = arguments['--ds-edge-compensation']
        if(not edge_compensation is None):
            edge_compensation = int(edge_compensation)

        filters_count = 0
        pass2_conf += filters_begin
        if(pass_nr in {1,2}):
            pass2_conf += deshaker_cfg.format(filters_count=filters_count, pass_nr=pass_nr, ms_h=ms_h, ms_v=ms_v, ms_r=ms_r, ms_z=ms_z, zoom_factor=zoom_factor, edge_compensation=edge_compensation, rolling_shutter=rolling_shutter, rolling_shutter_on=rolling_shutter_on)
            filters_count += 1
        if(smoother):
            pass2_conf += smoother_cfg.format(filters_count=filters_count)
            filters_count += 1
        pass2_conf += filters_end

        # print output
        print(pass2_conf)

    # Handle invalid options
    except docopt.DocoptExit as e:
        print (e)
