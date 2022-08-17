cd "D:\Programs\Python\Twitch"
venv\Scripts\activate
While ($True){
	cd "D:\Programs\Python\Twitch\CLIPS89"
	python main_cycled.py
	sleep 60
	cd "D:\Programs\Python\Twitch\FREAK_CLIPS"
	python freak_main_cycled.py
	sleep 7200
}