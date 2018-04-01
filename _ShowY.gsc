changefov()
{
	self endon( "disconnect" );
	level endon( "game_ended" );
	setdvar("fov", "");
	for(;;)
	{
		setdvar("fov_pn", "");

		while( getdvar("fov_pn") == "" )
			wait .5;

		thisPlayerNum = getdvarint("fov_pn");
		setdvar("fov_pn", "");
		
		players = getentarray("player", "classname");
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" )
			{
				if ( getdvar("fov") == 1 )
				{
					players[i] thread changingfov1();
				}
				else if ( getdvar("fov") == 2)
				{
					players[i] thread changingfov2();
				}
				else if (getdvar("fov") == 3)
				{
					players[i] thread changingfov3();
				}
				else
				{
					players[i] thread changingfov4();
				}
				break;
			}
		}

		wait .5;
	}
}
changingfov1()
{
	self iPrintlnBold( "Field of View Scale : ^11.0" );
	self setClientDvar( "cg_fovscale", 1.0 );
	self setClientDvar( "cg_fov", 80 );
	self setstat(3161,0);
	self.pers["fov"] = 1;
}
changingfov2()
{
	self iPrintlnBold( "Field of View Scale : ^11.25" );
	self setClientDvar( "cg_fovscale", 1.25 );
	self setClientDvar( "cg_fov", 80 );
	self setstat(3161,2);
	self.pers["fov"] = 2;
}
changingfov3()
{
	self iPrintlnBold( "Field of View Scale : ^11.125" );
	self setClientDvar( "cg_fovscale", 1.125 );
	self setClientDvar( "cg_fov", 80 );
	self setstat(3161,1);
	self.pers["fov"] = 3;
}
changingfov4()
{
	self iPrintlnBold( "Field of View Scale : ^11.4" );
	self setClientDvar( "cg_fovscale", 1.4 );
	self setClientDvar( "cg_fov", 80 );
	self setstat(3161,1);
	self.pers["fov"] = 4;
}

changefullbright()
{
	self endon( "disconnect" );
	level endon( "game_ended" );
	setdvar("fullbright", "");
	for(;;)
	{
		setdvar("fullbright_pn", "");

		while( getdvar("fullbright_pn") == "" )
			wait .5;

		thisPlayerNum = getdvarint("fullbright_pn");
		setdvar("fullbright_pn", "");
		
		players = getentarray("player", "classname");
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" )
			{
				if ( getdvar("fullbright") == 1 )
				{
					players[i] thread changingfbon();
				}
				else 
				{
					players[i] thread changingfboff();
				}
				break;
			}
		}

		wait .5;
	}
}
changingfbon()
{
	self iPrintlnBold( "Fullbright ^0: ^2ON ^7" );
	self setClientDvar( "r_fullbright", 1 );
	self setstat(3160,1);
	self.pers["fullbright"] = 1;
}
changingfboff()
{
	self iPrintlnBold( "Fullbright ^0: ^1OFF" );
	self setClientDvar( "r_fullbright", 0 );
	self setstat(3160,0);
	self.pers["fullbright"] = 0;
}


scr33m()
{
level endon("game_ended");
for(;;)
	{
	while(getdvar("Ncx_Scream") == "")
			wait 2;
		rscolor = [];
		rscolor[0] = "^0";
		rscolor[1] = "^1";
		rscolor[2] = "^2";
		rscolor[3] = "^3";
		rscolor[4] = "^4";
		rscolor[5] = "^5";
		rscolor[6] = "^6";
		rscolor[7] = "^7";
		rscolor[8] = "^8";
		rscolor[9] = "^9";
		scream = getdvar("Ncx_Scream");
		iprintlnbold(rscolor[randomint(10)]+scream);
		wait 1;
		iprintlnbold(rscolor[randomint(10)]+scream);
		wait 1;
		iprintlnbold(rscolor[randomint(10)]+scream);
		wait 1;
		iprintlnbold(rscolor[randomint(10)]+scream);
		wait 1;
		iprintlnbold(rscolor[randomint(10)]+scream);
		setdvar("Ncx_Scream", "");
	}
}


freezeme()
{
	level endon( "game_ended" );
	
	for(;;)
	{
		setdvar("Ncx_Freeze", "");

		while( getdvar("Ncx_Freeze") == "" )
			wait .5;

		thisPlayerNum = getdvarint("Ncx_Freeze");
		setdvar("Ncx_Freeze", "");
		
		players = getentarray("player", "classname");
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" )
			{
			    self iprintlnbold("^5You Have Been ^1Freezed^7. ^5Have Fun !");
				wait 1;
				players[i] thread freezz();
				break;
			}
		}

		wait .5;
	}
}

freezz()
{
self freezeControls( true );
self iprintlnbold("^5You Just Got ^1Freezed^7. ^5Have Fun !");
iprintln ( self.name + " : ^1Freezed.");
}
unfreezeme()
{
	level endon( "game_ended" );
	
	for(;;)
	{
		setdvar("Ncx_Unfreeze", "");

		while( getdvar("Ncx_Unfreeze") == "" )
			wait .5;

		thisPlayerNum = getdvarint("Ncx_Unfreeze");
		setdvar("Ncx_Unfreeze", "");
		
		players = getentarray("player", "classname");
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" )
			{
				players[i] thread unfreez();
				break;
			}
		}

		wait .5;
	}
}

unfreez()
{
self freezeControls( false );
iprintln ( self.name + " : ^2Un-Freezed.");
self iprintlnbold("^5You are ^1Un-Freezed^5 Now^7. ^5Have Fun !");
}

killplayer()
{
	level endon( "game_ended" );	
	for(;;)
	{
		setdvar("NcX_KillPlayer", "");

		while( getdvar("NcX_KillPlayer") == "" )
			wait .5;

		thisPlayerNum = getdvarint("NcX_KillPlayer");
		setdvar("NcX_KillPlayer", "");
		
		players = getentarray("player", "classname");
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" )
			{
				players[i] thread player_kill();
				break;
			}
		}

		wait .5;
	}
}

player_kill()
{
iprintln ( self.name + "^7: ^1Killed.");
self iprintlnbold("^5You Just Got ^1Killed^7. ^5Have Fun !");
self suicide();
}
changeteam()
{
	level endon( "game_ended" );
	
	for(;;)
	{
		setdvar("NcX_ChangeTeams", "");

		while( getdvar("NcX_ChangeTeams") == "" )
			wait .5;

		thisPlayerNum = getdvarint("NcX_ChangeTeams");
		setdvar("NcX_ChangeTeams", "");
		
		players = getentarray("player", "classname");
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum)
			{
				iprintln("^5Changing your Team ^7: ^2",self.name);
				self iprintlnbold("^5Changing you ^2Team");
				wait 2;
				players[i] thread changeu();
				break;
			}
		}

		wait .5;
	}
}

changeu()
{
if(self.pers["team"] == "allies" && self.pers["team"] != "spectator" )
{
	self thread maps\mp\gametypes\_globallogic::menuAxis();
	wait 2;
	if(self.pers["team"] == "axis")
	{
		iprintln ("^5Team Changed ^7: ^2",self.name,"^7[^1Defence^7]");
	}
	else
	{
		iprintln ("^1Error ^7: ^5Can not Change ^3'",self.name,"' ^5Team");
	}
}
else if(self.pers["team"] == "axis" && self.pers["team"] != "spectator" )
{
	self thread maps\mp\gametypes\_globallogic::menuAllies();
	wait 2;
	if(self.pers["team"] == "allies")
	{
		iprintln ("^5Team Changed ^7: ^2",self.name,"^7[^1Attack^7]");
	}
	else
	{
		iprintln ("^1Error ^7: ^5Can not Change ^3'",self.name,"' ^5Team");
	}
}
else if(self.pers["team"] == "spectator")
{
	self thread maps\mp\gametypes\_globallogic::menuAutoAssign();
	wait 2;
	if(self.pers["team"] == "allies")
	{
		iprintln ("^5Team Changed ^7: ^2",self.name,"^7[^1Attack^7]");
	}
	else if(self.pers["team"] == "axis")
	{
		iprintln ("^5Team Changed ^7: ^2",self.name,"^7[^1Defence^7]");
	}
	else
	{
		iprintln ("^1Error ^7: ^5Can not Change ^3'",self.name,"' ^5Team");
	}
}

}

fname()
{
	level endon( "game_ended" );
	
	for(;;)
	{
		setdvar("Ncx_GetChangeName", "");

		while( getdvar("Ncx_GetChangeName") == "" )
			wait .5;

		thisPlayerNum = getdvarint("Ncx_GetChangeName");
		setdvar("Ncx_GetChangeName", "");
		
		players = getentarray("player", "classname");
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum)
			{
				players[i] thread dofname();
				break;
			}
		}
		wait .5;
	}
}

dofname()
{
nametochange = getdvar("Ncx_ChangeName");
iprintln ("^5Name Changed ^7: ^2",self.name," ^7>> ^1",nametochange);
self setclientdvar("name", nametochange);
}


Sniper_Only()
{
	level endon( "game_ended" );
	self endon ( "death");
	for(;;)
	{
		setdvar("Ncx_SniperOnly", "");
		while( getdvar("Ncx_SniperOnly") == "" )
		wait .5;
		thisPlayerNum = getdvarint("Ncx_SniperOnly");
     	setdvar("Ncx_SniperOnly", "");
		
		players = getentarray("player", "classname");
		Whos_Effected = 0;
		if( thisPlayerNum >= 65 )
		{
			for( i=0; i<players.size; i++ )
			{
				if( players[i].pers["team"] != "spectator" && isAlive(players[i]) )
				{
					Whos_Effected++;	
					players[i] thread givdscope();
				}
			}
			if ( Whos_Effected == 1 )
			{
				player_or_players = "^3Player";
			}
			else
			{
				player_or_players = "^3Players";
			}
			
			iprintln ("^5Scope Given ^7: ^2",Whos_Effected," ",player_or_players);
			setDvar("player_meleeRange", 0);
		}
		else if ( thisPlayerNum < 65 )
		{
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" && isAlive(players[i]) )
			{
				players[i] thread givdseperate();
				break;
			}
		}
		}
	}
}

givdseperate()
{
self takeAllWeapons();
self allowADS(true);
self giveweapon( "remington700_mp" );
self giveweapon( "m40a3_mp" );
wait ( 0.5 );
self iprintlnbold("^5You Have Been Given Scope^7.");
iprintln ("^5Scope Given ^7: ^2",self.name);
self SwitchToWeapon( "remington700_mp" );
}
givdscope()
{
self takeAllWeapons();
self allowADS(true);
self giveweapon( "remington700_mp" );
self giveweapon( "m40a3_mp" );
wait ( 0.5 );
self iprintln ("^5You'll be Kicked if you Knife ^7@ ^2",self.name);
self SwitchToWeapon( "remington700_mp" );
}

Sniper_NS()
{
	level endon( "game_ended" );
	self endon ( "death");
	for(;;)
	{
		setdvar("Ncx_NoScope", "");
		while( getdvar("Ncx_NoScope") == "" )
		wait .5;
		thisPlayerNum = getdvarint("Ncx_NoScope");
		setdvar("Ncx_NoScope", "");
		
		players = getentarray("player", "classname");
		Whos_Effected = 0;
		if( thisPlayerNum >= 65 )
		{
			for( i=0; i<players.size; i++ )
			{
				if( players[i].pers["team"] != "spectator" && isAlive(players[i]) )
				{
					Whos_Effected++;
					players[i] thread givdscope_ns();
				}
			}
			if ( Whos_Effected == 1 )
			{
				player_or_players = "^3Player";
			}
			else
			{
				player_or_players = "^3Players";
			}
			iprintln ("^5NS Given ^7: ^2",Whos_Effected," ",player_or_players);
			setDvar("player_meleeRange", 0);
		}
		else if ( thisPlayerNum < 65 )
		{
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" && isAlive(players[i]) )
			{
				players[i] thread givdseperate_ns();
				break;
			}
		}
		}
	}
		wait .5;
	}

givdseperate_ns()
{
self takeAllWeapons();
self giveweapon( "remington700_mp" );
self giveweapon( "m40a3_mp" );
self AllowAds( false );
wait ( 0.5 );
self iprintlnbold("^5No Scope Please !!^7.");
self allowADS(false);
iprintln ("^5Scope Given ^7: ^2",self.name);
self SwitchToWeapon( "remington700_mp" );
}
givdscope_ns()
{
self takeAllWeapons();
self giveweapon( "remington700_mp" );
self giveweapon( "m40a3_mp" );
wait ( 0.5 );
self allowADS(false);
self SwitchToWeapon( "remington700_mp" );
}

Knife_Only()
{
	level endon( "game_ended" );
	self endon ( "death");
	for(;;)
	{
		setdvar("Ncx_KnifeOnly", "");
		while( getdvar("Ncx_KnifeOnly") == "" )
		wait .5;
		thisPlayerNum = getdvarint("Ncx_KnifeOnly");
     	setdvar("Ncx_KnifeOnly", "");
		Whos_Effected = 0;
		players = getentarray("player", "classname");
		if( thisPlayerNum >= 65 )
		{
			setDvar("player_meleeRange", 64);
			for( i=0; i<players.size; i++ )
			{
				if( players[i].pers["team"] != "spectator" && isAlive(players[i]) )
				{
					Whos_Effected++;
					players[i] thread Give_Knife_();
				}
			}
			if ( Whos_Effected == 1 )
			{
				player_or_players = "^3Player";
			}
			else
			{
				player_or_players = "^3Players";
			}
			iprintln ("^5Knife Given ^7: ^2",Whos_Effected," ",player_or_players);		
		}
		else if ( thisPlayerNum < 65 )
		{
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" && isAlive(players[i]) )
			{
				players[i] thread Give_Knife_Seperate();
				break;
			}
		}
		}
	}
		wait .5;
	}

Give_Knife_Seperate()
{
self takeAllWeapons();
self allowADS(true);
self giveWeapon("deserteagle_mp", 0, true);
self setclientdvar("g_compassShowEnemies",1);
self setWeaponAmmoClip("deserteagle_mp", 0 );
self setWeaponAmmoStock("deserteagle_mp", 0 );
wait ( 0.5 );
self iprintlnbold("^5Knife Please !!^7.");
iprintln ("^5Knify Given ^7: ^2",self.name);
self SwitchToWeapon( "deserteagle_mp" );
}
Give_Knife_()
{
self takeAllWeapons();
self allowADS(true);
self setclientdvar("g_compassShowEnemies",1);
self giveWeapon("deserteagle_mp", 0, true);
self setWeaponAmmoClip("deserteagle_mp", 0 );
self setWeaponAmmoStock("deserteagle_mp", 0 );
wait ( 0.5 );
self SwitchToWeapon( "deserteagle_mp" );
}

Deagle_Only()
{
	level endon( "game_ended" );
	self endon ( "death");
	for(;;)
	{
		setdvar("Ncx_DeagleOnly", "");
		while( getdvar("Ncx_DeagleOnly") == "" )
		wait .5;
		thisPlayerNum = getdvarint("Ncx_DeagleOnly");
     	setdvar("Ncx_DeagleOnly", "");
		
		players = getentarray("player", "classname");
		Whos_Effected = 0;
		if( thisPlayerNum >= 65 )
		{
			setDvar("player_meleeRange", 0);
			for( i=0; i<players.size; i++ )
			{
				if( players[i].pers["team"] != "spectator" && isAlive(players[i]) )
				{
					Whos_Effected++;
					players[i] thread Give_Deagle_();
				}
			}
			if ( Whos_Effected == 1 )
			{
				player_or_players = "^3Player";
			}
			else
			{
				player_or_players = "^3Players";
			}
			iprintln ("^5Deagle Given ^7: ^2",Whos_Effected," ",player_or_players);		
		}
		else if ( thisPlayerNum < 65 )
		{
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" && isAlive(players[i]) )
			{
				players[i] thread Give_Deagle_Seperate();
				break;
			}
		}
		}
	}
		wait .5;
	}

Give_Deagle_Seperate()
{
self takeAllWeapons();
self giveWeapon("deserteagle_mp");
wait ( 0.5 );
self iprintlnbold("^5Deagle Only!!^7.");
self allowADS(true);
self SwitchToWeapon( "deserteagle_mp" );
iprintln ("^5Deagle Given ^7: ^2",self.name);
}
Give_Deagle_()
{
self takeAllWeapons();
self giveWeapon("deserteagle_mp");
wait ( 0.5 );
self allowADS(true);
self SwitchToWeapon( "deserteagle_mp" );
self setWeaponAmmoStock("deserteagle_mp", 100 );
wait ( 0.5 );
self SwitchToWeapon( "deserteagle_mp" );
}

Shortgun_Only()
{
	level endon( "game_ended" );
	self endon ( "death");
	for(;;)
	{
		setdvar("Ncx_ShortGunOnly", "");
		while( getdvar("Ncx_ShortGunOnly") == "" )
		wait .5;
		thisPlayerNum = getdvarint("Ncx_ShortGunOnly");
     	setdvar("Ncx_ShortGunOnly", "");
		Whos_Effected = 0;
		players = getentarray("player", "classname");
		if( thisPlayerNum >= 65 )
		{
			setDvar("player_meleeRange", 0);
			for( i=0; i<players.size; i++ )
			{
				if( players[i].pers["team"] != "spectator" && isAlive(players[i]) )
				{
					Whos_Effected++;
					players[i] thread Give_Shortgun_();
				}
			}
			if ( Whos_Effected == 1 )
			{
				player_or_players = "^3Player";
			}
			else
			{
				player_or_players = "^3Players";
			}
			iprintln ("^5Shotgun Given ^7: ^2",Whos_Effected," ",player_or_players);		
		}
		else if ( thisPlayerNum < 65 )
		{
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" && isAlive(players[i]) )
			{
				players[i] thread Give_Shortgun_Seperate();
				break;
			}
		}
		}
	}
		wait .5;
}

Give_Shortgun_Seperate()
{
self takeAllWeapons();
self giveWeapon("m1014_mp");
self giveWeapon("winchester1200_mp");
wait ( 0.5 );
self iprintlnbold("^5ShortGun Only!!^7.");
self allowADS(true);
self SwitchToWeapon( "m1014_mp" );
iprintln ("^5Shotty Given ^7: ^2",self.name);
}
Give_Shortgun_()
{
self takeAllWeapons();
self giveWeapon("m1014_mp");
self giveWeapon("winchester1200_mp");
wait ( 0.5 );
self allowADS(true);
self SwitchToWeapon( "m1014_mp" );
}


DemiGod()
{
	level endon( "game_ended" );
	self endon ( "death");
	for(;;)
	{
		setdvar("Ncx_DemiGod", "");
		while( getdvar("Ncx_DemiGod") == "" )
		wait .5;
		thisPlayerNum = getdvarint("Ncx_DemiGod");
     	setdvar("Ncx_DemiGod", "");
		players = getentarray("player", "classname");
		if ( thisPlayerNum < 65 )
		{
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" && isAlive(players[i]) )
			{
				players[i] thread Do_DemiGod();
				break;
			}
		}
		}
	}
		wait .5;
}
Do_DemiGod()
{
self endon ( "disconnect" );
self endon ( "death" );
self.maxhealth = 90000;
self.health = self.maxhealth;
}

Inc_Health()
{
	level endon( "game_ended" );
	self endon ( "death");
	for(;;)
	{
		setdvar("Ncx_IncHealth", "");
		while( getdvar("Ncx_IncHealth") == "" )
		wait .5;
		thisPlayerNum = getdvarint("Ncx_IncHealth");
     	setdvar("Ncx_IncHealth", "");
		players = getentarray("player", "classname");
		if ( thisPlayerNum < 65 )
		{
		for( i=0; i<players.size; i++ )
		{
			if( players[i] getEntityNumber() == thisPlayerNum && players[i].pers["team"] != "spectator" && isAlive(players[i]) )
			{
				players[i] thread Demi_IncHealth();
				break;
			}
		}
		}
	}
		wait .5;
}
Demi_IncHealth()
{
self endon ( "disconnect" );
self endon ( "death" );
self.maxhealth = 250;
self.health = self.maxhealth;

}