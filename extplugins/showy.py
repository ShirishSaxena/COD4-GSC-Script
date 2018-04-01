
__version__ = '3.0'
__author__  = 'Mr.ShowOff'

import b3, re, time
import b3.plugin
import thread
import threading
import b3.events
import b3.cron
import datetime
import json
import urllib2

#--------------------------------------------------------------------------------------------------
class ShowyPlugin(b3.plugin.Plugin):
	_adminPlugin = None
	_minLevel_sl = None
	_minLevel_allalias = None
	_minLevel_sban = None
	_minLevel_lb = None
	_minLevel_notices = None
	_minLevel_pastbans = None
	_minLevel_listids = None
        
	def startup(self):
		"""\
		Initialize plugin settings
		"""
                
		# get the plugin so we can register commands
		self._adminPlugin = self.console.getPlugin('admin')
		if not self._adminPlugin:
			# something is wrong, can't start without admin plugin
			self.error('Could not find admin plugin')
			return False
		
		# get the minium level allowed to use this plugin
		self.verbose('Getting config options')
                # register our commands
		self.verbose('Registering commands')
                if 'Showy' in self.config.sections():
                        self.verbose('Registering Showy_ShowY')
                        for cmd in self.config.options('Showy'):
                                level = self.config.get('Showy', cmd)
                                sp = cmd.split('-')
                                alias = None
                                if len(sp) == 2:
                                        cmd, alias = sp
                                func = self.getCmd(cmd)
                                if func:
                                        self._adminPlugin.registerCommand(self, cmd, level, func, alias)

                if 'For_NcxMod' in self.config.sections():
                        self.verbose('Registering NcxMod_ShowY')
                        for cmd in self.config.options('For_NcxMod'):
                                level = self.config.get('For_NcxMod', cmd)
                                sp = cmd.split('-')
                                alias = None
                                if len(sp) == 2:
                                        cmd, alias = sp
                                func = self.getCmd(cmd)
                                if func:
                                        self._adminPlugin.registerCommand(self, cmd, level, func, alias)

                if 'Mostly_For_Promod' in self.config.sections():
                        self.verbose('Registering For_Promod_ShowY')
                        for cmd in self.config.options('Mostly_For_Promod'):
                                level = self.config.get('Mostly_For_Promod', cmd)
                                sp = cmd.split('-')
                                alias = None
                                if len(sp) == 2:
                                        cmd, alias = sp
                                func = self.getCmd(cmd)
                                if func:
                                        self._adminPlugin.registerCommand(self, cmd, level, func, alias)

                if 'Extra' in self.config.sections():
                        self.verbose('Registering Extra_ShowY')
                        for cmd in self.config.options('Extra'):
                                level = self.config.get('Extra', cmd)
                                sp = cmd.split('-')
                                alias = None
                                if len(sp) == 2:
                                        cmd, alias = sp
                                func = self.getCmd(cmd)
                                if func:
                                        self._adminPlugin.registerCommand(self, cmd, level, func, alias)

                
                self._adminPlugin.registerCommand(self, 'ncxhost', '0', self.cmd_ncxhost, 'ncx')
		self.Load_banwatcher()
		
		self.debug('Started : Ncx Host Plugin')
		self.console.say('^1Ncx Host ^5Plugin v2.3 ^7: ^2Started')

        def getCmd(self, cmd):
            cmd = 'cmd_%s' % cmd
            if hasattr(self, cmd):
              func = getattr(self, cmd)
              return func

            return None
	def onEvent(self,  event):
		if event.type == b3.events.EVT_CLIENT_AUTH:
			self.tell_notices(event.client)
		elif event.type == b3.events.EVT_CLIENT_BAN_TEMP or event.type == b3.events.EVT_CLIENT_BAN:
			self.tell_bans(event.client)

	def  Load_banwatcher(self):
			self.registerEvent(b3.events.EVT_CLIENT_BAN)
			self.registerEvent(b3.events.EVT_CLIENT_BAN_TEMP)
			
	def get_player_bans(self,  client):
		cursor = self.console.storage.query(
		"""SELECT a.name, p.reason, p.time_expire  FROM penalties p, clients a
		WHERE a.id = p.admin_id AND (p.type = "tempban" OR p.type = "ban") AND p.client_id = %s """%(client.id))
		bans = []
		if cursor.rowcount > 0:
			while not cursor.EOF:
				r = cursor.getRow()
				bans.append("^2%s ^7for ^4%s ^7until ^3%s" %(r['name'],  r['reason'],  self.console.formatTime(r['time_expire'])))
				cursor.moveNext()
		cursor.close()
		return bans
	
	def tell_bans(self, client):
		a = self._adminPlugin.getAdmins()
		bans = self.get_player_bans(client)

		if len(a) > 0 and len(bans) > 0:
			for adm in a:
				adm.message("^1%s ^7: ^4%s ^7past bans"  %(client.name,  len(bans)))

	
	def cmd_pastbans(self, data, client, cmd=None):
		"""\
		<name> - list all player's past bans
		"""
		if not self.console.storage.status():
			cmd.sayLoudOrPM(client, '^1Error ^7: ^5Database DOWN')
			return False		
		
		m = self._adminPlugin.parseUserCmd(data)
		if not m:
			client.message('^1Error ^7: ^5Name Not Supplied')
			return False
	
		cid = m[0]
		sclient = self._adminPlugin.findClientPrompt(cid, client)
		if not sclient:
			return
		
		bans = self.get_player_bans(sclient)
		
		if len(bans) == 0:
			cmd.sayLoudOrPM(client, "^1Error ^7: ^5%s ^7Never been banned" % sclient.exactName)
			return True
			
		cmd.sayLoudOrPM(client, "^7%s past bans:" %(sclient.exactName))
		for b in bans:
			cmd.sayLoudOrPM(client,  b)

	def cmd_superlookup(self,  data,  client,  cmd=None):
		"""\
		<name> - search players that have used or are using that name
		"""
		if not self.console.storage.status():
			cmd.sayLoudOrPM(client, '^1Error ^7: ^5Database DOWN')
			return False
		if not len(data):
			client.message('^1Error ^7: ^5Player name not Supplied!')
			return False

		#Get all players that are currently using that name
		clients = self.console.clients.lookupByName(data)
		
		#Get all players that have used the alias
		cursor = self.console.storage.query("""SELECT c.id, c.name, a.time_edit FROM clients c, aliases a WHERE c.id = a.client_id && a.alias LIKE '%%%s%%'"""%(data))

		if cursor.rowcount == 0 and len(clients) == 0:
			cmd.sayLoudOrPM(client,  "^1Error ^7: ^5No Player have used this alias")
			return
		
		ids = []
		
		if len(clients) > 0:
			cmd.sayLoudOrPM(client, "Players that are currently using %s: " % (data))
			for c in clients:
				cmd.sayLoudOrPM(client, "^7[^2@%s^7] %s (^3%s^7)" % (c.id,  c.exactName,  self.console.formatTime(c.timeEdit)))
				ids.append(c.id)
		else:
			cmd.sayLoudOrPM(client, "^1Error ^7: No Player have used this alias%s" % (data))
		
		if cursor.rowcount > 0:
			cmd.sayLoudOrPM(client, "Players that have used %s: " % (data))
			while not cursor.EOF:
				msg = ""
				r = cursor.getRow()
				if not (int(r['id'] ) in ids):
					msg += "^7[^2@%s^7] %s (^3%s^7)" % (r['id'],  r['name'],  self.console.formatTime(r['time_edit']))
					cmd.sayLoudOrPM(client,  msg)
					ids.append(int(r['id']))
				cursor.moveNext()
		else:
			cmd.sayLoudOrPM(client, "^1Error ^7: No Player have used this alias%s" % (data))

		cursor.close()
		
	def cmd_allaliases(self, data, client=None, cmd=None):
		"""\
		<name> [<detailed>] - list all player's aliases
		"""
		if not self.console.storage.status():
			cmd.sayLoudOrPM(client, '^1Error ^7: ^5Database DOWN')
			return False		
		
		m = self._adminPlugin.parseUserCmd(data)
		if not m:
			client.message('^1Error ^7: ^5Name Not Supplied')
			return False
	
		cid = m[0]
		sclient = self._adminPlugin.findClientPrompt(cid, client)
		if not sclient:
			return
		
		cursor = self.console.storage.query("""SELECT a.alias, a.time_add, a.time_edit, a.num_used FROM aliases a WHERE a.client_id = %s """%(sclient.id))
		if cursor.rowcount == 0:
			cmd.sayLoudOrPM(client, '^1%s^7: ^5No aliases Found' % sclient.exactName)
			return True
			
		if not m[1]:
			aliases = []
			while not cursor.EOF:
				r = cursor.getRow()
				aliases.append("^7%s" % r['alias'])
				cursor.moveNext()

			cmd.sayLoudOrPM(client, "^7%s aliases: %s" %(sclient.exactName, ', '.join(aliases)))
		else:
			cmd.sayLoudOrPM(client, "^7%s aliases:" %(sclient.exactName))
			while not cursor.EOF:
				r = cursor.getRow()
				cmd.sayLoudOrPM(client, "^7%s, added ^3(%s) ^7last ^7modified ^3(%s) ^7used ^3%s ^7times" %(r['alias'], self.console.formatTime(r['time_add']), self.console.formatTime(r['time_edit']),  r['num_used']+1))
				cursor.moveNext()
		
		cursor.close()

	def cmd_superbaninfo(self, data, client=None, cmd=None):
		"""\
		<name> - Give information about player's active bans
		"""
		if not self.console.storage.status():
			cmd.sayLoudOrPM(client, '^1Error ^7: ^5Database DOWN')
			return False

		m = self._adminPlugin.parseUserCmd(data)
		if not m:
			client.message('^1Error ^7: ^5Name Not Supplied')
			return False

		sclient = self._adminPlugin.findClientPrompt(m[0], client)
		if sclient:
			numbans = sclient.numBans
			if numbans:
				cmd.sayLoudOrPM(client, '^2%s ^7: ^1%s active bans found' % (sclient.exactName, numbans))
				bans = sclient.bans
				for b in bans:
					admin = self.console.storage.getClientsMatching({ 'id' : b.adminId })[0].name					
					cmd.sayLoudOrPM(client,  '^7Banned by ^2%s ^7until ^3%s ^7for ^7reason ^1%s' % (admin,   self.console.formatTime(b.timeExpire),  b.reason))
				
			else:
				cmd.sayLoudOrPM(client, '%s : ^5No Active Bans' % sclient.exactName)

		
	def cmd_listbans(self, data, client=None, cmd=None):
		"""\
		[<name>] [<type>] - list all active bans, if name specified, list all active bans by that admin; type can be 'ban' or 'tempban', tempban is the default.
		"""
		if not self.console.storage.status():
			cmd.sayLoudOrPM(client, '^1Error ^7: ^5Database DOWN')
			return False
		
		adm = ""
		ban = "TempBan"
		if data:
			m = self._adminPlugin.parseUserCmd(data)
			
			if m[0]:
				cid = m[0]
				sclient = self._adminPlugin.findClientPrompt(cid, client)
			
				adm = "AND p.admin_id = %s" % sclient.id
			
			if m[1]:
				if m[1] == "ban":
					ban = "Ban"
				elif m[1] == "tempban":
					ban = "TempBan"
				else:
					cmd.sayLoudOrPM(client, "^1Error ^7: Wrong type of Ban. Must be 'ban' | 'tempban'")
					return False
		
		#Get all players that have active bans
		cursor = self.console.storage.query("""
		SELECT c.id, c.name, p.time_expire, p.reason
		FROM penalties p, clients c 
		WHERE p.client_id = c.id AND
		p.inactive = 0 AND 
		type='%s' AND
		p.time_expire >= UNIX_TIMESTAMP() %s""" % (ban, adm))

		if cursor.rowcount == 0:
			cmd.sayLoudOrPM(client, "^1Error ^7: No Active Bans")
			return
		
		cmd.sayLoudOrPM(client, "^1Active Ban ^7: ^5%s" % cursor.rowcount)
		while not cursor.EOF:
			r = cursor.getRow()
			msg = "^7[^2@%s^7] %s (until ^3%s^7) ^7for ^7%s" % (r['id'],  r['name'],  self.console.formatTime(r['time_expire']),  r['reason'])
			cmd.sayLoudOrPM(client,  msg)

			cursor.moveNext()

		cursor.close()
		
	def cmd_listids(self,  data, client, cmd=None):
		"""\
		[name] - Lists player IDs or name's ID
		"""
		if not self.console.storage.status():
			cmd.sayLoudOrPM(client, '^1Error ^7: ^5Database DOWN')
			return False

		m = self._adminPlugin.parseUserCmd(data)
		if not m:
			clientes = []
			for c in self.console.clients.getList():
				clientes.append("^7%s: ^2@%d^7" %(c.exactName,  c.id))
			cmd.sayLoudOrPM(client,  ", ".join(clientes))
			return True
	
		cid = m[0]
		sclient = self._adminPlugin.findClientPrompt(cid, client)
		if not sclient:
			return
		cmd.sayLoudOrPM(client,  "^7%s: ^2@%d" % (sclient.exactName, sclient.id))

        def cmd_balance(self, data, client, cmd=None):
          """\
          ^2Force Balance Teams
          """ 
          self.console.write('Ncx_Balance 1')
          cmd.sayLoudOrPM(client, '^2Balancing ^5Teams')
          return True

        def cmd_irkhost(self, data, client, cmd=None):
          """\
          Usage : !ncxhost xfire/founders/website
          """ 
          if data == 'xfire':
            cmd.sayLoudOrPM(client, '^1Xfire : ^5mrshowoff15 ^7| ^5happyskumawat')
          elif data == 'founders':
            cmd.sayLoudOrPM(client, '^1Founder : ^5Mr.ShowOff ^7| ^5Happy')
          elif data == 'website':
            cmd.sayLoudOrPM(client, '^1Website : ^1Ncx^2Host^7.in')
          else:
                cmd.sayLoudOrPM(client, '^1Website : ^1Ncx^2Host^7.in')
                cmd.sayLoudOrPM(client, '^1Founder : ^5Mr.ShowOff ^7| ^5Happy')
                cmd.sayLoudOrPM(client, '^1Xfire : ^5mrshowoff15 ^7| ^5happyskumawat')
          return True

        def cmd_scr33m(self, data, client, cmd=None):
              """\
              Scream Something on Center
              """
              if not data:
                  client.message('^2Enter something you Hoe')
                  return False

              if data:
                  cmd.sayLoudOrPM(client, '^2Screaming : ^5%s' % (data))
                  self.console.write('set Ncx_Scream %s'% (data))
                  return True
              return True

        def cmd_fastrestart(self, data, client, cmd=None):
            """\
            Fastly Restart the Current map
            """
            self.console.say('^5Fast Restart ^7: ^5 Enjoy 1st Knife Round')
            time.sleep(2) 
            self.console.write('fast_restart')
            time.sleep(3.5)
            self.console.say('^5Fast Restart ^7: ^6Successful')
            return True
        def cmd_ff(self, data, client, cmd=None):
            """
            Set Friendly Fire { Team kill }
            Usage : ^5on ^7| ^5off ^7| ^5shared ^7| ^5reflect
            """
            if not data:
              client.message('^1Error ^7: Usage =>> ^5on ^7| ^5off ^7| ^5shared ^7| ^5reflect')
              return False
            else:
              input = data.split(' ',1)
              if input[0] == 'off' :
                  self.console.say('^2Set Friendly Fire^1 Off')
                  time.sleep(2) 
                  self.console.write('scr_team_fftype 0')
                  return True
              if input[0] == 'on' : 
                  self.console.say('^2Set Friendly Fire^1 On')
                  time.sleep(2)
                  self.console.write('scr_team_fftype 1')
                  return True
              if input[0] == 'shared' : 
                  self.console.say('^2Set Friendly Fire^1 Shared')
                  time.sleep(2)
                  self.console.write('scr_team_fftype 2')
                  return True
              if input[0] == 'reflect' : 
                  self.console.say('^2Set Friendly Fire^1 Reflect')
                  time.sleep(2)
                  self.console.write('scr_team_fftype 3')
                  return True
              client.message('^7Invalid data, type off,on,shared or reflect')   
            return True
        def cmd_killcam(self, data, client, cmd=None):
            """
            Enable or Disable KillCam !
            Usage : !killcam on { Turn's Killcam On }
            """
            if not data:
              client.message('^1Error ^7: ^5After Command Use !killcam on/off')
              return False
            else:
              input = data.split(' ')
              if input[0] == 'on' :
                  self.console.say('^1Killcam ^7: ^2On')
                  time.sleep(2) 
                  self.console.write('scr_game_allowkillcam 1')
                  return True
              if input[0] == 'off' : 
                  self.console.say('^1Killcam ^7: ^2Off')
                  time.sleep(2)
                  self.console.write('scr_game_allowkillcam 0')
                  return True
                  client.message('^1Error ^7: ^5After Command Use !killcam on/off')    
            return True
        def cmd_gametype(self, data, client, cmd=None):
            """
            Change Gametype of Server
            Usage : !gametype sab|sd|dm|tdm|hq
            """
            if not data:
              client.message('^1Error ^7: ^5Try ^7!gametype sab|sd|dm|tdm|hq')
              return False
            else:
              input = data.split(' ')
              if input[0] == 'sab' :
                  self.console.say('^2Gamtype Changed ^7: ^1 Sabotage')
                  time.sleep(2)
                  self.console.write('g_gametype sab')
                  self.console.write('map_restart')
                  return True 
              if input[0] == 'sd' : 
                  self.console.say('^2Gamtype Changed ^7: ^1Search and Destroy')
                  time.sleep(2)
                  self.console.write('g_gametype sd')
                  self.console.write('map_restart')
                  return True 
              if input[0] == 'dm' : 
                  self.console.say('^2Gamtype Changed ^7:^1 Death Match')
                  time.sleep(2)
                  self.console.write('g_gametype dm')
                  self.console.write('map_restart')
                  return True 
              if input[0] == 'tdm' : 
                  self.console.say('^2Gamtype Changed ^7:^1 Team Deathmatch')
                  time.sleep(2)
                  self.console.write('g_gametype war')
                  self.console.write('map_restart')
                  return True 
              if input[0] == 'hq' : 
                  self.console.say('^2Gamtype Changed ^7:^1 Headquater')
                  time.sleep(2)
                  self.console.write('g_gametype koth')
                  self.console.write('map_restart')
                  return True 
              client.message('^1Error ^7: ^5Try ^7!gametype sab|sd|dm|tdm|hq')     
            return True
        
        def cmd_spectate(self, data, client, cmd=None):
            """\
            Set Spectating Value
            Usage : !spectate off|free|team
            """
            if not data:
              client.message('^1Error ^7: try !spectate off|free|team ')
              return False
            else:
              input = data.split(' ')
              if input[0] == 'off' :
                  self.console.say('^2Spectate ^7:^1 Off')
                  time.sleep(2) 
                  self.console.write('scr_game_spectatetype 0')
                  self.console.write('fast_restart')
                  return True
              if input[0] == 'team' : 
                  self.console.say('^2Spectate ^7:^1 Team')
                  time.sleep(2)
                  self.console.write('scr_game_spectatetype 1')
                  self.console.write('fast_restart')
                  return True
              if input[0] == 'free' : 
                  self.console.say('^2Spectate ^7:^1 Free')
                  time.sleep(2)
                  self.console.write('scr_game_spectatetype 2')
                  self.console.write('fast_restart')
                  return True
              client.message('^1Error ^7: try !spectate off|free|team ')
            return True
	
        def cmd_plimit(self, data, client, cmd=None):
          """\
          Set Limit to Gun's
          Usage : !limit sniper|assault|specops|demolitions ^1no { No = No of Guns per team }
          Example -:
            !limit assault 5
          """
          str = data.split(' ',1)
          
          if str[0] == 'assault':
            self.console.say('^5Assault limit ^7: ^1%s' %str[1])
            self.console.write('class_assault_limit %s' %str[1])
          elif str[0] == 'specops':
            self.console.say('^5SpecOps limit ^7: ^1%s' %str[1])
            self.console.write('class_specops_limit %s' %str[1])
          elif str[0] == 'demolitions':
            self.console.say('^5Demolitions limit ^7: ^1%s' %str[1])
            self.console.write('class_demolitions_limit %s' %str[1])
          elif str[0] == 'sniper':
            self.console.say('^5Sniper limit ^7: ^1%s' %str[1])
            self.console.write('class_sniper_limit %s' %str[1])
          else:
            cmd.sayLoudOrPM(client, '^1Usage : {sniper|assault|specops|demolitions} integer')
          return True

        def cmd_mag(self, data, client, cmd=None):
            """\
            Loads a map with a gametype.
            !mag shipment hq
            """
            if not data:
              client.message('^7Missing data, type off or on behind the command')
              return False
            else:
              input = data.split(' ',1)  
              map = input[0]
              input[0] = 'mp_%s'% input[0]
              #---------------------------------------
              if input[1] == 'tdm' : input[1] = 'war'
              if input[1] == 'hq' : input[1] = 'koth'
              #----------------------------------------
              if input[1] == 'sab' : gametype = 'Sabotage'
              if input[1] == 'war' : gametype = 'Team Deathmatch'
              if input[1] == 'koth' : gametype = 'Headquaters'
              if input[1] == 'sd' : gametype = 'Search and destroy'
              if input[1] == 'dm' : gametype = 'Deathmatch'
              if input[1] != '' :
                  #self.console.say('^2Map will change to^3 %s ^2gametype^3 %s'% (map,gametype))
                  self.console.say('^5Map Changed ^7:^2 %s,'% map)
                  self.console.say('^5Gametype Changed ^7:^2 %s'% gametype)
                  time.sleep(1)
                  self.console.write('g_gametype "%s"'% input[1])
                  time.sleep(1)
                  self.console.write('map %s'% input[0])
                  return True   
            return True
        def cmd_freeze(self, data, client, cmd=None):
                """\
                <player> Freeze a Player
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                if not data:
                    client.message('^1Error ^7: ^5You must supply a players name or number')
                    return False

                if m:
                    sclient = self._adminPlugin.findClientPrompt(m[0], client)
		    if sclient.maxLevel >= client.maxLevel:
                            client.message('^7%s ^7is a masked higher level player, can\'t Freeze | NooB Alert !' % client.exactName)
		    else :
                            self.console.write('Ncx_Freeze %s' % (sclient.cid))
			    cmd.sayLoudOrPM(client, '^5Freezed ^7: ^1%s' % (sclient.exactName))
                else:
                    client.message('Player not found')
                    return False
        def cmd_unfreeze(self, data, client, cmd=None):
                """\
                <player> UnFreeze a Player
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                
                if not data:
                    client.message('^1Error ^7: ^5You must supply a players name or number')
                    return False

                if m:
                        sclient = self._adminPlugin.findClientPrompt(m[0], client)
			if sclient.maxLevel >= client.maxLevel:
				if sclient.maskGroup:
					client.message('^7%s ^7is a masked higher level player, can\'t UnFreeze | NooB Alert !' % client.exactName)
				else:
					#self.console.say(self.getMessage('ban_denied', client.exactName, sclient.exactName))
					client.message('^7 ^7Unknown Error : Contact Mr.ShowOff | Xfire: mrshowoff15' )
			else :
				self.console.write('Ncx_Unfreeze %s' % (sclient.cid))
				cmd.sayLoudOrPM(client, '^5Un-Freezed ^7: ^2%s' % (sclient.exactName))
                else:
                    client.message('Player not found')
                    return False
        def cmd_killp(self, data, client, cmd=None):
                """\
                <player> Kill A Player
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                
                if not data:
                    client.message('^1Error ^7: ^5You must supply a players name or number')
                    return False

                if m:
                        sclient = self._adminPlugin.findClientPrompt(m[0], client)
                        if sclient.maxLevel >= client.maxLevel:
                                if sclient.maskGroup:
                                        client.message('^7%s ^7is a masked higher level player, can\'t UnFreeze | NooB Alert !' % client.exactName)
				else:
					#self.console.say(self.getMessage('ban_denied', client.exactName, sclient.exactName))
					client.message('^7 ^7Unknown Error : Contact Mr.ShowOff | Xfire: mrshowoff15' )
                        else :
                                self.console.write('NcX_KillPlayer %s' % (sclient.cid))
                                cmd.sayLoudOrPM(client, '^5Killed ^7: ^1%s' % (sclient.exactName))
                else:
                    client.message('Player not found')
                    return False
        def cmd_sniperonly(self, data, client, cmd=None):
                """\
                <player> Work's Only on NcxMod. Ncx Sniper Only Mod
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                
                if not data:
                    self.console.write('Ncx_SniperOnly 1000')
                    cmd.sayLoudOrPM(client, '^8#iRk Sniper Only ^7 :^2Enabled For One Spawn')
                    return False

                if m:
                    sclient = self._adminPlugin.findClientPrompt(m[0], client)
                    self.console.write('Ncx_SniperOnly %s' % (sclient.cid))
                    cmd.sayLoudOrPM(client, '^8Scope Given ^7: ^2%s' % (sclient.exactName))
                    return True
                else:
                    client.message('Player not found')
                    return False
        def cmd_nsonly(self, data, client, cmd=None):
                """\
                <player> Work's Only on NcxMod. Ncx No Scope Sniper Only Mod
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                
                if not data:
                    self.console.write('Ncx_NoScope 1000')
                    cmd.sayLoudOrPM(client, '^8#iRk NS Only ^7 :^2Enabled For One Spawn')
                    return False

                if m:
                    sclient = self._adminPlugin.findClientPrompt(m[0], client)
                    self.console.write('Ncx_NoScope %s' % (sclient.cid))
                    cmd.sayLoudOrPM(client, '^8NS Sniper Given ^7: ^2%s' % (sclient.exactName))
                    return True
                else:
                    client.message('Player not found')
                    return False
        def cmd_knifeonly(self, data, client, cmd=None):
                """\
                <player> Work's Only on NcxMod. Ncx Knife Only Mod
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                
                if not data:
                    self.console.write('Ncx_KnifeOnly 1000')
                    cmd.sayLoudOrPM(client, '^8#iRk Knife Only ^7 :^2Enabled For One Spawn')
                    return False

                if m:
                    sclient = self._adminPlugin.findClientPrompt(m[0], client)
                    self.console.write('Ncx_KnifeOnly %s' % (sclient.cid))
                    cmd.sayLoudOrPM(client, '^8Knife Given ^7: ^2%s' % (sclient.exactName))
                    return True
                else:
                    client.message('Player not found')
                    return False
        def cmd_deagleonly(self, data, client, cmd=None):
                """\
                <player> Work's Only on NcxMod. Ncx Deagle Only Mod
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                
                if not data:
                    self.console.write('Ncx_DeagleOnly 1000')
                    cmd.sayLoudOrPM(client, '^8Ncx Deagle Only ^7 :^2Enabled For One Spawn')
                    return False
                if m:
                    sclient = self._adminPlugin.findClientPrompt(m[0], client)
                    self.console.write('Ncx_DeagleOnly %s' % (sclient.cid))
                    cmd.sayLoudOrPM(client, '^8 #iRk Deagle Given ^7: ^2%s' % (sclient.exactName))
                    return True
                else:
                    client.message('Player not found')
                    return False
        def cmd_shotgunonly(self, data, client, cmd=None):
                """\
                <player> Work's Only on NcxMod. Ncx Shotgun Only Mod
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                
                if not data:
                    self.console.write('Ncx_ShortGunOnly 1000')
                    cmd.sayLoudOrPM(client, '^8#iRk Shotgun Only ^7 :^2Enabled For One Spawn')
                    return False

                if m:
                    sclient = self._adminPlugin.findClientPrompt(m[0], client)
                    self.console.write('Ncx_ShortGunOnly %s' % (sclient.cid))
                    cmd.sayLoudOrPM(client, '^8Shotty Given ^7: ^2%s' % (sclient.exactName))
                    return True
                else:
                    client.message('Player not found')
                    return False
        def cmd_changeteams(self, data, client, cmd=None):
                """\
                <player> Work's Only on NcxMod. Change Given Player Team
                """
                m = self._adminPlugin.parseUserCmd(data)
                
                if not data:
                    cmd.sayLoudOrPM(client, '^1Error ^7: ^5No Player Specified !')
                    return False
                if m:
                        sclient = self._adminPlugin.findClientPrompt(m[0], client)
                        if sclient.maxLevel >= client.maxLevel:
                                if sclient.maskGroup:
                                        client.message('^7%s ^7is a masked higher level player, can\'t Changeteam | NooB Alert !' % client.exactName)
                                else:
                                        #self.console.say(self.getMessage('ban_denied', client.exactName, sclient.exactName))
                                        client.message('^7 ^7Unknown Error : Contact 7584844588' )
			else :
				self.console.write('NcX_ChangeTeams %s' % (sclient.cid))
				cmd.sayLoudOrPM(client, '^5Team Changed ^7: ^2%s' % (sclient.exactName))
                else:
                    client.message('Player not found')
                    return False
        def cmd_changename(self, data, client, cmd=None):
                """\
                <player> Work's Only on NcxMod. Change Given Player Name
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                
                if not data:
                    cmd.sayLoudOrPM(client, '^1Error ^7: ^5No Player Specified !')
                    return False

                if m :
                    sclient = self._adminPlugin.findClientPrompt(m[0], client)
                    self.console.write('Ncx_ChangeName %s' % (m[1]))
                    self.console.write('Ncx_GetChangeName %s' % (sclient.cid))
                    cmd.sayLoudOrPM(client, '^8Name Changed ^7: ^2%s ^7>> ^1%s' % (sclient.exactName,m[1]))
                    return True
                else:
                    client.message('Usage: !changename nameofplayer nametochange')
                    return False
        def cmd_getip(self, data, client, cmd=None):
                """
                <name> - Find details about player IP
                """
                m = self._adminPlugin.parseUserCmd(data)
                if not m:
                        client.message('^7Invalid parameters, you must supply a player name')
                        return False
                sclient = self._adminPlugin.findClientPrompt(m[0], client)
                
                if sclient:
                        url = 'http://ip-api.com/json/%s' %( sclient.ip )
                        data = json.load(urllib2.urlopen(url))
                        Status = data['status']
                        if Status == 'success' :
                                City = data['city']
                                Zip = data['zip']
                                CountryCode = data['countryCode']
                                Country = data['country']
                                Region = data['region']
                                ISP = data['isp']
                                Longitude = data['lon']
                                Latitude = data['lat']
                                TimeZone = data['timezone']
                                AS = data['as']
                                Query = data['query']
                                Organization = data['org']
                                RegionName = data['regionName']
                                if not City :
                                        City = 'Unknown'
                                if not Zip :
                                        Zip = 'Unknown'
                                if not CountryCode:
                                        CountryCode = 'null'
                                if not Country:
                                        Country = 'Unknown'
                                if not Region :
                                        Region = 'Unknown'
                                if not ISP :
                                        ISP = 'Unknown'
                                if not TimeZone :
                                        TimeZone = 'Unknown'
                                if not AS :
                                        AS = 'Unknown'
                                if not Organization :
                                        Organization = 'Unknown'
                                if RegionName :
                                        cmd.sayLoudOrPM(client, '^3IP   ^7: %s (%s)' %(Query,sclient.exactName))
                                        cmd.sayLoudOrPM(client, '^3City ^7: %s (%s)' %(RegionName,City))
                                        cmd.sayLoudOrPM(client, '^3ISP  ^7: %s (%s)' %(ISP,Country))
                                else:
                                        cmd.sayLoudOrPM(client, '^3IP   ^7: %s (%s)' %(Query,sclient.exactName))
                                        cmd.sayLoudOrPM(client, '^3City ^7: %s     ' %(City))
                                        cmd.sayLoudOrPM(client, '^3ISP  ^7: %s (%s)' %(ISP,Country))
                        else :
                                Error = data['message']
                                Status = 'Fail'
                                if Error == 'private range' :
                                        Error = 'Private Range'
                                        Description = 'The IP address is part of a private range'
                                elif Error == 'reserved range' :
                                        Error = 'Reserved Range'
                                        Description = 'The IP address is part of a reserved range'
                                elif Error == 'invalid query':
                                        Error = 'Invalid Query'
                                        Description = 'Invalid IP address or Domain name'
                                elif Error == 'quota' :
                                        Error = 'Over Quota'
                                        Description = 'Over Quota'
                                else :
                                        Error = data['message']
                                        Description = data['message']
                                cmd.sayLoudOrPM(client, '^3Error : %s (%s)' %(data['query'],Description))

                return True
        def cmd_fov(self, data, client, cmd=None):
                """\
                <player> Changes FOV
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                if not data:
                    client.message('^1Error ^7: ^5You must supply a players name or number')
                    return False

                if m:
                        sclient = self._adminPlugin.findClientPrompt(m[0], client)
                        self.console.write('fov_pn %s' % (sclient.cid))
                        cmd.sayLoudOrPM(client, '^5Freezed ^7: ^1%s' % (sclient.exactName))
                else:
                    client.message('Player not found')
                    return False
        def cmd_fov(self, data, client, cmd=None):
                """\
                <player> Work's Only on NcxMod. Toggle Fov
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                
                if not data:
                    cmd.sayLoudOrPM(client, '^1Error ^7: ^5Specify FOV [1,1.125,1.25,1.4]!')
                    return False

                if m :
                        sclient = client
                        if m[0] == 1:
                                self.console.write('fov 1')
                                self.console.write('fov_pn %s' % (sclient))
                                cmd.sayLoudOrPM(client, '^8Fov Set ^7: ^21.00' )
                        elif m[0] == 1.125:
                                self.console.write('fov 3')
                                self.console.write('fov_pn %s' % (sclient))
                                cmd.sayLoudOrPM(client, '^8Fov Set ^7: ^21.125' )
                        elif m[0] == 1.25:
                                self.console.write('fov 2')
                                self.console.write('fov_pn %s' % (sclient))
                                cmd.sayLoudOrPM(client, '^8Fov Set ^7: ^21.25' )
                        elif m[0] == 1.4:
                                self.console.write('fov 4')
                                self.console.write('fov_pn %s' % (sclient))
                                cmd.sayLoudOrPM(client, '^8Fov Set ^7: ^21.4' )
                    return True
                else:
                    client.message('Usage: !fullbright 1.25,1,4,1,1.125')
                    return False

        def cmd_fullbright(self, data, client, cmd=None):
                """\
                <player> Work's Only on NcxMod. Toggle Fullbright
                """
                
                m = self._adminPlugin.parseUserCmd(data)
                
                if not data:
                    cmd.sayLoudOrPM(client, '^1Error ^7: ^5Specify Fullbright [On,Off]!')
                    return False

                if m :
                        sclient = client
                        if m[0] == 1 or m[0] == "On" or m[0] == "on" or m[0] == "ON":
                                self.console.write('fullbright 1')
                                self.console.write('fullbright_pn %s' % (sclient))
                                cmd.sayLoudOrPM(client, '^8Fullbright ^7: ^2ON' )
                        else:
                                self.console.write('fullbright 2')
                                self.console.write('fullbright_pn %s' % (sclient))
                                cmd.sayLoudOrPM(client, '^8Fullbright ^7: ^2OFF' )
                    return True
                else:
                    client.message('Usage: !fullbright On,Off')
                    return False


