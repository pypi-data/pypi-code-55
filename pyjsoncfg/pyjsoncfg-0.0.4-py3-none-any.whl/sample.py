
import os
import sys

from pyjsoncfg import Config


if __name__=='__main__':
    
    os.environ.setdefault(Config.PYJSONCONFIG_BASE,"~")
    cfg = Config( filename="sample_cfg.json", auto_conv=True, not_exist_ok=False ) 
        
    print( cfg.exists() )
    cfg.savefd(sys.stdout)
    
    c = cfg.val(["dummy_array"], defval=[] )
    print( "array", c, type(c))
    
    c1 = cfg.int(["dummy_complex","a"], defval=4)
    print( "dummy_complex.a", c1, type(c1))

    c2 = cfg.int(cfg("dummy_complex.a"), defval=4)
    print( "dummy_complex.a", c2, type(c2))
    
    assert( c1==c2 )
    assert( type(c1)==type(c2) )

    c = cfg.bool(["dummy_complex","e"], defval=5)
    print( "dummy_complex.e", c, type(c))

    print( "dummy_complex.a", cfg().dummy_complex.a )
    print( "dummy_complex.d.da", cfg().dummy_complex.d.da )
    print( "dummy_complex.d.db", cfg().dummy_complex.d.db )

    c1 = cfg().dummy_complex.d.db = "test1"
    print( "dummy_complex.d.db", cfg().dummy_complex.d.db )
    c2 = cfg().dummy_complex.d.db = "test2"
    print( "dummy_complex.d.db", cfg().dummy_complex.d.db )

    assert( c1!=c2 )
    assert( type(c1)==type(c2) )

    #

    for k,v in cfg().dummy_complex.items():
        print("dummy_complex", k,v)

    print( cfg()["dummy_array"] )
    print( cfg.val(["dummy_array"] ))
    
    print( cfg()["dummy_complex"] )
    print( cfg.val(["dummy_complex"] ))

    print( "navigation sample" )
    
    print( bool(cfg()["dummy_complex"]["d"]["dc"] )) # get the value as in json
    print( cfg.bool(["dummy_complex","d","dc"] )) # get interpreted as bool
    print( cfg.bool( cfg("dummy_complex.d.dc") )) # get interpreted as bool
    print( cfg.val( cfg("dummy_complex.d.dc") )) # get plain using selector
    print( cfg().dummy_complex.d.dc ) # get plain using namespace

    print( bool(cfg()["dummy_complex"]["d"]["dc_0"] )) # get the value as in json
    print( cfg.bool(["dummy_complex","d","dc_0"] )) # get interpreted as bool
    print( cfg.bool( cfg("dummy_complex.d.dc_0") )) # get interpreted as bool
    print( cfg.val( cfg("dummy_complex.d.dc_0") )) # get plain using selector
    print( cfg().dummy_complex.d.dc_0 ) # get plain using namespace

    print( bool(cfg()["dummy_complex"]["d"]["dc_1"] )) # get the value as in json
    print( cfg.bool(["dummy_complex","d","dc_1"] )) # get interpreted as bool
    print( cfg.bool( cfg("dummy_complex.d.dc_1") )) # get interpreted as bool
    print( cfg.val( cfg("dummy_complex.d.dc_1") )) # get plain using selector
    print( cfg().dummy_complex.d.dc_1 ) # get plain using namespace

    # write later to new config file with different name
    CFG_FILE = "sample2_cfg.json"
    try:
        fullpath = os.path.join( cfg.basepath, CFG_FILE )
        os.remove( fullpath )
    except:
        pass

    # only for this demo
    # save to different file
    cfg2 = Config( CFG_FILE, basepath=cfg.basepath, auto_conv=False )
    
    print( "exists", cfg2.exists() )
    print( cfg2 )
    
    # get shallow copy of the namespace, dont use !!!
    cfg2.data = cfg._namespace() 
    
    # shallow copy, reflects back to original
    assert( cfg2().a == cfg().a )
    cfg2().a = 1
    assert( cfg2().a == cfg().a )
    
    c1 = cfg.val(["dummy_array"],defval=[1])
    print( "array", c2, type(c2))
    
    cfg2().dummy_array.append(17)
    c2 = cfg2().dummy_array
    print( "array", c2, type(c2))
    
    assert( len(c1) == len(c2) ) 
    
    c = cfg2.int(["dummy_complex","a"],defval=4)
    print( "dummy_complex.a", c, type(c))

    cfg.savefd(sys.stdout)
    cfg2.savefd(sys.stdout)
    
    # sanitize 
    print( "santize normal" )
    cfg2.sanitize()
    cfg2.savefd(sys.stdout)
    
    # sanitize 'secret' keyword in addition to default keywords
    print( "santize again" )
    cfg2.sanitize(["secret"])
    
    # print
    cfg2.savefd(sys.stdout)
    
    print("-"*7)
    
    # sample code 
    val_a = cfg().dummy_complex.a 
    cfg().dummy_complex.a += 1
    val_a_after = cfg().dummy_complex.a 
    print( "a before", val_a, "after", val_a_after )

    val_array = []
    val_array.extend( cfg().dummy_array )
    cfg().dummy_array.append(175)
    val_array_after = cfg().dummy_array
    print( "array before", val_array, "after", val_array_after )

    print( bool(cfg()["dummy_complex"]["d"]["dc"] )) # get the value as in json
    print( cfg.bool(["dummy_complex","d","dc"] )) # get interpreted as bool
    print( cfg.bool( cfg("dummy_complex.d.dc") )) # get interpreted as bool
    print( cfg.val( cfg("dummy_complex.d.dc") )) # get plain using selector
    print( cfg().dummy_complex.d.dc ) # get plain using namespace

### dict style

    # property dc is in the config file
    v = cfg()["dummy_complex"]["d"]["dc"]
    print(v,type(v))

### string selector

    # property de is new here!
    v = cfg.val( ["dummy_complex","d","de"], defval=False ) # with default value
    print(v,type(v))

### property string selector

    # property de is not new here, no chamge since created above
    v = cfg.val( cfg("dummy_complex.d.de"), defval=True ) # with default value, 
    print(v,type(v))

### namespace selector

    v = cfg().dummy_complex.d.de
    print(v,type(v))      

### dict handling

    cfg()["z"] = { "a": 1 }    
    cfg()["zx"] = { "a" : 1, "b" : { "c" : 2 }}
    
    cfg().zx.b.update({ "c": 3, "d": 4, "e" : 5 })

    del cfg().zx.b.c

    print( cfg().zx.b.items() ) 
    print( type( cfg().zx.b ) )
    print( type( cfg().zx.b.items() ) )
    
    # iterate 
    for k,v in cfg().zx.b.items():
        print(k,v)
    
    print( type( cfg().zx.b.e ) )

    print( "e" in cfg().zx.b ) 
    print( "f" in cfg().zx.b ) 

### expand vars

    # print structure of substsample config setting
    print( "subst var sample:", cfg().substsample )
    # subst all vars in substsample setting within a single call
    print( "result:", cfg.expand( cfg().substsample ) )
    
    # or more complicated...
    # get all vars in the string as tupel
    vars = cfg.getexpandvars( cfg().substsample ) # `eval_str` is populated with config value for substsample setting
    print( "vars:", vars )
    # get all vars and values as tupel
    exvars = cfg.expandvars( vars ) 
    print( "expandvars", exvars )
    # if required manipulate expandvars beforehand
    print( "result:", cfg.expand( cfg().substsample, expandvars=exvars ) )

    # nested or referencing vars
    print( "referencing:", cfg().substsample2 ) 
    print( "result referencing:", cfg.expand( cfg().substsample2 ) )

    # nested or referencing vars with endless loop due to self-referencing
    # stops at `recursion_level=3`
    print( "self-referencing:", cfg().substsample3 ) 
    print( "result self-referencing:", cfg.expand( cfg().substsample3 ) )

    # save to disk
    cfg2.save()
    
   