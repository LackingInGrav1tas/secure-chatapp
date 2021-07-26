# secure-chatapp
End-to-end encrypted chat app written with Flask

[site](https://secure-chatapp.herokuapp.com/)

for info go to the /info/ tab on the site.

NOTE: encryption is serverside NOT clientside. Because of this, it relies on Heroku's SSL to be truly e2ee.

-----------------------------------

The logs get first serialized then stored in redis (```r.set('log', pickle.dumps(log))```) because i dont think redis supports storage of 2D objects (```log``` is a hashmap containing lists)


-----------------------------------

![image](https://user-images.githubusercontent.com/42680395/126934701-b6c5bb4e-8f5f-43e8-86bb-e0f667625ac8.png)
