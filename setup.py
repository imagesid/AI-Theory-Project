from cx_Freeze import  Executable, setup

executables = [Executable("sprite.py")]

setup(
    name="Mini Game",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["ri 1.png","ri 2.png", "ri 3.png","le 1.png","le 2.png",
                                            "le 3.png","up 1.png","up 2.png","up 3.png","do 1.png",
                                            "do 2.png","do 3.png","bakc.png", "bg.mp3", "boom.wav", "high score.txt",
                                            "ri 11.png", "ye 1.png", "s.wav", "freesansbold.ttf"]}},
    version = "1.0.0",
    author = "Bereket G.",
    description = "Mini Game with Python 3.4",
    executables = executables

    )                                                                                                                                                                                                                                         
