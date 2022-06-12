
<div align="center"> <br>
  
  ![readme_top](https://user-images.githubusercontent.com/55090298/172143775-b2fbabea-e3bf-44c8-b19b-ef3bab8f7ba6.png)
  
  <span>2022-1-OSSProj-GaCo-3</span>
  
  ![title](https://user-images.githubusercontent.com/55090298/172143908-f758f8a7-ffa7-4c26-a1ae-3bb34920025c.png)
  
  <p> Here is a boy who wants to save his family and neighbors from cruel devil.<br>
      The Devil has destroyed other village to test his magical power.<br>
      The next target must be the boy's village.<br>
      The boy heads to the devil's castle to defeat the devil!</p>  

</div>
<br>

![readme_line](https://user-images.githubusercontent.com/55090298/172144122-10dfda4f-ef4b-497f-b29d-ce4bdc2f5f16.png)

<h1 id="table-of-contents"> :book: Table of Contents</h1>

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#lst1"> ➤ Support Operating Systems & Requirements</a></li>
    <li><a href="#lst2"> ➤ How to Install & Run the Game </a></li>
    <li><a href="#lst3"> ➤ Project Structure Summary </a></li>
    <li><a href="#vid" > ➤ Game overview : playing video</a></li>
    <li><a href="#lst4"> ➤ Game Detail : MENU </a></li>
    <li><a href="#lst5"> ➤ Game Detail : KEYs </a></li>
    <li><a href="#lst6"> ➤ Game Detail : RUN </a></li>
    <li><a href="#lst7"> ➤ Game Detail : RANK </a></li>
    <li><a href="#lst8"> ➤ Developers </a></li>
  </ol>
</details>

<br><br><br>

![readme_line_thin](https://user-images.githubusercontent.com/55090298/172147189-ec840b6f-467b-4b9f-ac45-cd7d3a8307df.png)





<h1 id="lst1"> :computer: Support Operating Systems & Requirements</h1>

<h2>1. OS</h2>
<p>OS that have installed python3</p>
<ul>
  <li><img src="https://img.shields.io/badge/Ubuntu-E95420?style=plastic&logo=Ubuntu&logoColor=white"/></li>
  <li><img src="https://img.shields.io/badge/macOS-000000?style=plastic&logo=macOS&logoColor=white"/></li>
  <li><img src="https://img.shields.io/badge/Windows-0078D6?style=plastic&logo=Windows&logoColor=white"/></li>
 </ul>
<br>

<h2>2. Requirements</h2>
<ul>
  <li>Library : pygame 2</li>
</ul>

<br><br><br>

![readme_line_thin](https://user-images.githubusercontent.com/55090298/172147189-ec840b6f-467b-4b9f-ac45-cd7d3a8307df.png)





<h1 id="lst2"> :game_die: How to Install & Run the Game</h1>

<h2>1. Install Python3</h2>
If you've already installed python3, go to <a href="#install-pygame"> 'Install PyGame2'</a>.
<ul>
  <li>Ubuntu</li>
  
  ```
  $ sudo apt-get update
  $ sudo apt install python3
  ```
  
  <li>macOS</li>
  
  ```
  $ brew update
  $ brew install python3
  ```
  
</ul>

<br>
<h2><span id="install-pygame">2. Install PyGame2</span></h2>
<ul>
  
```
$ pip3 install --upgrade pip3
$ pip3 install pygame
```
  
</ul>

<br>
<h2>3. Install '마왕의 성' Game</h2>
<ul>
  
```
$ git clone https://github.com/CSID-DGU/2022-1-OSSProj-GaCo-3
$ cd 2022-1-OSSProj-GaCo-3
$ python3 code/game.py
```
  
</ul>


<br><br><br>

![readme_line_thin](https://user-images.githubusercontent.com/55090298/172147189-ec840b6f-467b-4b9f-ac45-cd7d3a8307df.png)





<h1 id="lst3"> :open_file_folder: Project Structure Summary</h1>
  <h2><li>Project Structure Summary with tree</li></h2>
  <ul>
  
      .
      ├── README.md
      ├── code
      │   ├── AbyssSpell.py
      │   ├── Bringer.py
      │   ├── BringerSpell.py
      │   ├── Devil.py
      │   ├── Monster.py
      │   ├── abyss.py
      │   ├── debug.py
      │   ├── game.py
      │   ├── level.py
      │   ├── player.py
      │   ├── rank.py
      │   ├── scene.py
      │   ├── settings.py
      │   ├── sound.py
      │   ├── soundManager.py
      │   └── support.py
      ├── image
      │   ├── Monster
      │   │   ├── AbyssSpell
      │   │   │   ├── spell.png
      │   │   │   └── spellL.png
      │   │   ├── Devil
      │   │   │     └──...
      │   │   ├── abyss
      │   │   │     └──...
      │   │   └── bringer
      │   │         └──...
      │   ├── UI
      │   │     └──...
      │   ├── etc
      │   │     └──...
      │   ├── font
      │   │     └──...
      │   ├── map
      │   │     └──...
      │   └── player2
      │         └──...
      ├── rank
      │   └── user_score.txt
      └── sound
          ├── BGM
          │     └──...
          ├── abyss
          │     └──...
          ├── bringer
          │     └──...
          ├── default_hit.wav
          ├── player
          │     └──...
          └── sword_slash.wav


</ul>

<br><br><br>

![readme_line_thin](https://user-images.githubusercontent.com/55090298/172147189-ec840b6f-467b-4b9f-ac45-cd7d3a8307df.png)






<!-- 시연 영상 !-->
<h1 id="vid"> :video_game: Game overview : playing video</h1>

<ul><h3>youtube link : https://www.youtube.com/watch?v=wUAIkpjHn7o</h3></ul>

<br><br><br>

![readme_line_thin](https://user-images.githubusercontent.com/55090298/172147189-ec840b6f-467b-4b9f-ac45-cd7d3a8307df.png)







<h1 id="lst4"> :video_game: Game Detail : MENU</h1>
<ul>
<p align="justify">
    The beginning scene shows the title of the game. You can press 'Return key' to enter menu scene after passing through the story scene and key description scene. In the menu scene, you can access the story scene through the button in the upper left corner and the key description scene through the button in the upper right corner, and press 'Return key' to return to the menu. Also You can check the ranking by pressing the first button at the bottom. And click the middle button at the bottom to start the game. You can exit the game by pressing last button at the bottom. 
</p>

![menu](https://user-images.githubusercontent.com/55090298/173198493-29b22057-c58a-4480-ba09-1670499cd5ee.gif)
 
</ul>
<br><br><br>

![readme_line_thin](https://user-images.githubusercontent.com/55090298/172147189-ec840b6f-467b-4b9f-ac45-cd7d3a8307df.png)






<h1 id="lst5"> :video_game: Game Detail : KEYs</h1>
<ul>
  <p align="justify">
    Your player can use the following keys. You can move in each direction by pressing the 'LEFT' and 'RIGHT' keys. You can jump by pressing the 'SPACE' key. The 'a' key is the default attack, and the 's' key is the more powerful attack. If you clear the stage, you will absorb the magic used by the enemy and can use it at next stage by pressing the 'q' and 'w' keys.
  </p>

<img width="1392" alt="image" src="https://user-images.githubusercontent.com/55090298/173203027-5502c389-c248-4e9d-8e53-b446d12a8d13.png">

</ul>
<br><br><br>

![readme_line_thin](https://user-images.githubusercontent.com/55090298/172147189-ec840b6f-467b-4b9f-ac45-cd7d3a8307df.png)






<h1 id="lst6"> :video_game: Game Detail : RUN</h1>

<ul>
  <li><p align="justify">The game has three stages. Each stage has one Monster, and if you kill the Monster, you can move on to the next stage. The first stage, the second stage, has Devil's henchmen, and the final opponent, Devil, is in stage 3.</p></li>
  
  <h3><li>STAGE 1 - Abyss</li></h3>
  <p align="justify">The name of the monster in "STAGE 1" is Abyss. Abyss uses magic that blowing fireworks to the player and an attack that explodes when the player approaches. If you defeat Abyss, you can use Abyss's magic attack from the next stage.</p>
  
  ![stage1-re](https://user-images.githubusercontent.com/55090298/173200822-052595e8-0e2e-47a6-8e68-4a694308fa14.gif)
  
  <h3><li>STAGE 2 - Bringer</li></h3>
  <p align="justify">The name of the monster in "STAGE 2" is Bringer. Bringer uses a magic that dropping lightning on the player's position and uses a sword attack when the player is close. If you defeat Bringer, you can use Bringer's magic attack from the next stage.</p>
  
  ![stage2-re](https://user-images.githubusercontent.com/55090298/173200889-60c4d521-8263-4dab-b2ba-e407ddb902b6.gif)
  
  <h3><li>STAGE3 - Devil</li></h3>
  <p align="jusify">Stage3's Monster is Devil. Devil has four attacks. (1) Sword attack when the player is close. (2) A magical attack that stops the player from moving. (3) A magical attack dropping a huge lightning on the player's position. (4) A magical attack explodes the player's position.</p>
  
  (1) Sword attack when the player is close.
  
  ![stage3_attack(1)](https://user-images.githubusercontent.com/55090298/173202376-8c2edeae-ca6a-4ff9-a86b-0bbc5790f714.gif)
      
  <br><br>
  (2) A magical attack that stops the player from moving.
  
  ![stage3_attack2-2](https://user-images.githubusercontent.com/55090298/173201347-6f55888e-9532-4ae6-a565-16dbd7008419.gif)
  
  <br><br>
  (3) A magical attack dropping a huge lightning on the player's position.
  
  ![stage3_attack3](https://user-images.githubusercontent.com/55090298/173201380-08d59d0c-adc8-4448-b075-e2c4b43ab770.gif)
    
  <br><br>
  (4) A magical attack explodes the player's position.
  
  ![stage3_attack1](https://user-images.githubusercontent.com/55090298/173201343-3d7cd03a-e533-46b1-babd-f5beba8a34b2.gif)
  
  <br><br>
  <h3><li>WIN</li></h3>
  <p>If you clear all stages, Scene below will be shown on the screen. You can save your score. Also you can go back to the main menu by clicking the button at the upper left corner.(Details on <a href="#lst7">here</a>)</p>
  
  <img width="1392" alt="image" src="https://user-images.githubusercontent.com/55090298/173202854-ff356751-55d6-4628-b0dd-9f8298d6b650.png">
  
  <br><br>
  <h3><li>LOSE</li></h3>
  <p>If you lose, Scene below will be shown on the screen. You can move on to the main menu scene by pressing 'RETURN' key.</p>
  
  <img width="1392" alt="image" src="https://user-images.githubusercontent.com/55090298/173203002-9e5b737a-9965-4573-8f76-b426a6574176.png">

  
</ul>
<br><br><br>

![readme_line_thin](https://user-images.githubusercontent.com/55090298/172147189-ec840b6f-467b-4b9f-ac45-cd7d3a8307df.png)









<h1 id="lst7"> :video_game: Game Detail : RANK</h1>

<ul>
  <p align="justify">A timer starts to work when stage starts. You can check this timer on the upper right corner on stage scenes. If the player clears all stages, the timer stops and shows the score to the 'WIN' scene. If you type your name in the name input box and click the Save button in the bottom middle, the corresponding score will be saved. If your score is 10th or higher, you can check your name and score in the 'RANKING' scene which is accessible from the menu. If the score is outside the 10th place, the score disappears from the record and cannot be checked.</p>
  <br><br>
  <span align="center">
  
  ![timer](https://user-images.githubusercontent.com/55090298/173204326-904b885f-f35f-4db1-9d5d-7152aadcde45.gif)
  
  </span>
  <br><br>
  
  ![rank-win](https://user-images.githubusercontent.com/55090298/173204012-9dc39232-78aa-4b3e-a2d6-3af44de6038a.gif)

  <br><br>
  <p align="justify">The image below is the 'RANKING' scene. You can see the record up to 10th place. You can clear all records by pressing the initialization button in the upper right corner. You can go back to the main menu by clicking the button at the upper left corner.</p>
  
  ![rank-log](https://user-images.githubusercontent.com/55090298/173203898-e852a89d-051e-4dad-ad58-a7cd7c68923c.gif)

</ul>
<br><br><br>

![readme_line_thin](https://user-images.githubusercontent.com/55090298/172147189-ec840b6f-467b-4b9f-ac45-cd7d3a8307df.png)







<h1 id="lst8"> :busts_in_silhouette: Developers </h1>

* 박용준(Yongjun Park) <a href="https://github.com/Parkteams"><img src="https://img.shields.io/badge/github-181717?style=flat-square&logo=Github&logoColor=white"/></a>

* 서상민(Sangmin Seo) <a href="https://github.com/SeoSangmin"><img src="https://img.shields.io/badge/github-181717?style=flat-square&logo=Github&logoColor=white"/></a>

* 유재헌(Jaeheon Yu) <a href="https://github.com/midnight774"><img src="https://img.shields.io/badge/github-181717?style=flat-square&logo=Github&logoColor=white"/></a>

<br><br><br>
