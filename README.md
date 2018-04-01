# COD4-GSC-Script

Some Functions of cod4 that you can have fun around with on your own server.

Plugins are provided in folder called extplugins.
Plugin is for BigBrotherBot [B3]


-> To Use this Scripts in your own server
Put this script '_showy.gsc' to maps/mp/gametype/
Add these links to _globallogic.gsc
```
	thread maps\mp\gametypes\_ShowY::scr33m();
	thread maps\mp\gametypes\_ShowY::freezeme();
	thread maps\mp\gametypes\_ShowY::fname();
	thread maps\mp\gametypes\_ShowY::killplayer();
	thread maps\mp\gametypes\_ShowY::changeteam();
	thread maps\mp\gametypes\_ShowY::Sniper_Only();
	thread maps\mp\gametypes\_ShowY::Knife_Only();
	thread maps\mp\gametypes\_ShowY::Sniper_NS();
	thread maps\mp\gametypes\_ShowY::Shortgun_Only();
	thread maps\mp\gametypes\_ShowY::Deagle_Only();
	thread maps\mp\gametypes\_ShowY::unfreezeme();
	thread maps\mp\gametypes\_ShowY::DemiGod();
	thread maps\mp\gametypes\_ShowY::Inc_Health();
```

Save,compile and run
