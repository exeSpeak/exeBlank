# CONFIG FILE
# ALL VARIABLES ARE INTEGERS
# group= defines a category of variables, so that if you need to iterate through all variables of a certain type, the system has already separated them
# id= defines the identification name of a variable; no duplicates; used with vars_getMe, vars_addMe, and vars_setMe
# type= defines the type of a variable; must be identical to a defined group name
# value= defines the starting value of a variable at the beginning of a new game

window_assumed_width = 1280
window_assumed_height = 720
window_fps = 60
window_title = "My Awesome Game"

thisgame_application = (
    "id=dateTimeDisplayFormat::default=%Y-%m-%d",
    "id=defaultWindowWidth::default=1600",
    "id=defaultWindowHeight::default=900",
    "id=startFullScreen::default=True",
    "id=startLogoDeveloper::default=False",
    "id=startLogoPublisher::default=False",
    "id=visibleMenuBuar::default=False",
    "id=volumeMusic::default=0.5",
    "id=volumeSFX::default=0.5"
)

thisGame_application_fonts = (
    "id=01::file=fonts/PressStart2P-Regular.ttf",
    "id=02::file=fonts/PressStart2P-Bold.ttf"
)

thisgame_achievements = (
    "id=wowrich::gold>1000",
    "id=wowstrong::health>1000",
    "id=wowtank::armor>1000"
)

thisgame_audio_music = (
    "id=themeMainMenu::file=audio/music/mainTheme.mp3",
    "id=themePause::file=audio/music/pauseTheme.mp3"
)

thisgame_audio_sfx = (
    "id=thump::file=audio/sfx/thump.wav"
)

thisGame_collectables = (
    "id=feathers::location=home",
    "id=gnome01::location=townhall",
    "id=gnome02::location=townhall",
    "id=gnome03::location=townhall",
    "id=gnome04::location=townhall"
)

thisGame_crafting_recipes = (
    "id=barBronze::file=recipe/barBronze.json",
    "id=barIron::file=recipe/barIron.json",
    "id=barSteel::file=recipe/barSteel.json"
)

thisGame_crafting_resources = (
    "id=004::type=ore::name=aluminum",
    "id=005::type=ore::name=bronze",
    "id=006::type=ore::name=iron",
    "id=007::type=ore::name=steel",
    "id=008::type=ore::name=onyx",
    "id=009::type=ore::name=diamond"
)

thisGame_currencies = (
    "id=currency_gold::value=0",
    "id=currency_ore::value=10",
    "id=currency_scrap::value=10"
)

thisGame_dialogs = (
    "id=loadingScreen::dialog/loadingScreen.json",
    "id=newGame1::dialog/newgame1.json",
    "id=day01::dialog/day01.json"
)

thisGame_enemies = (
    "group=zombie::health=40::armor=0::damage=5",
    "group=pirate::health=50::armor=10::damage=7",
    "group=taxman::health=1000::armor=500::damage=100"
)

thisGame_flags = (
    "id=isGameRunning::default=False",
    "id=isGameSaving::default=False",
    "id=isGameLoaded::default=False",
    "id=isTutorialDisabled::default=False"
)

thisGame_equipable_armor = (
    "id=013::type=armor::name=helmet::tradeGold=5",
    "id=014::type=armor::name=chestplate::tradeGold=10",
    "id=015::type=armor::name=leggings::tradeGold=10",
    "id=016::type=armor::name=boots::tradeGold=5"
)

thisGame_equipable_weapons = (
    "id=010::type=weapon::name=sword::tradeGold=10",
    "id=011::type=weapon::name=dagger::tradeGold=5",
    "id=012::type=weapon::name=bow::tradeGold=15"
)

# THESE ARE THE DEFAULT KEYBINDINGS
thisGame_keybindings = (
    "key=escape::pressID=mainmenu",
    "key=space::pressID=jump",
    "key=e::pressID=walkup",
    "key=s::pressID=walkleft",
    "key=d::pressID=walkdown",
    "key=f::pressID=walkright",
    "key=g::pressID=interact",
    "key=z::pressID=inventory",
    "key=x::pressID=skills",
    "key=c::pressID=quests",
    "key=m::pressID=map",
    "key=/::pressID=help"
)

thisGame_locations = (
    "group=area",
    "group=building",
    "group=level",
    "id=001::area=home::file=home.json",
    "id=002::area=city::file=city.json",
    "id=012::building=townhall::file=townhall.json",
    "id=013::building=booth1::file=booth1.json",
    "id=014::building=booth2::file=booth2.json",
    "id=level01::type=level::file=level1.json"
)

thisGame_npcs = (
    "group=cityfolk",
    "group=vendor",
    "group=trainer",
    "id=gus::type=vendor",
    "id=mayor::type=cityfolk"
)

thisGame_quests = (
    "id=tutorial001::file=quests/tutorial1.json",
    "id=quest001::file=quests/quest1.json",
    "id=quest002::file=quests/quest2.json"
)

thisGame_skills = (
    "id=strength::name=strength::value=1",
    "id=dexterity::name=dexterity::value=1",
    "id=intelligence::name=intelligence::value=1"
)

thisGame_sprites = (
    "id=logo_homepage::file=sprites/logo_homepage.png",
    "id=player_happy::file=sprites/player_happy.png",
    "id=gusSprites::type=spritesheet::file=sprites/gus.png"
)

thisGame_stats = (
    "id=level::value=1",
    # DEPLETABLES
    "id=health::value=100",
    "id=health_max::value=100",
    "id=magic::value=100",
    "id=magic_max::value=100",
    "id=shield::value=0",
    "id=shield_max::value=100",
    "id=evasion::value=0",
    "id=evasion_max::value=100",
    "id=armor::value=100",
    "id=armor_max::value=100"
)

thisGame_statusEffects_buffs = (
    "id=heal::duration=10::instant=5",
    "id=regen::duration=10::ps=1",
    "id=shield::duration=10::instant=8",
    "id=hidden::duration=10",
    "id=armor::duration=10::instant=15"
)

thisGame_statusEffects_debuffs = (
    "id=freeze::duration=3::instant=12",
    "id=burn::duration=4::dps=4",
    "id=shocked::duration=2::dps=6",
    "id=poison::duration=10::dps=7",
    "id=bleed::duration=10::dps=5",
    "id=stun::duration=1::dps=0",
    "id=slow::duration=10::dps=0",
    "id=confusion::duration=10::dps=0",
    "id=blind::duration=10::dps=0"
)

thisGame_timers = (
    "id=countdown_quest::type=seconds",
    "id=time_played::type=seconds"
)