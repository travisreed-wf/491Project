ISU Web Portal
===
### Primary Contributors
* Andrew Guibert
* Andrew Hartman
* Jonathan Mielke
* Lucas Rorhet
* Travis Reed 

===
### Resources
* [Trello Board](https://trello.com/b/kPAKvBao/senior-design)
* [Group Website](http://may1518.ece.iastate.edu/)
* [Project Plan](https://drive.google.com/a/iastate.edu/file/d/0B6mbCLySBSQxOUxYQ196eUY5cXc/view?usp=sharing)

===
### Deplyoment Instructions
1. Package the source folder locally <br>
`zip build-MM-DD.zip ./src`
2. Transfer archive to vrac server <br>
`scp ./build-MM-DD.zip username@nirwebportal.vrac.iastate.edu:/home/nirwebportal/archives/`
3. SSH into nirwebportal.vrac.iastate.edu <br>
`ssh username@nirwebportal.vrac.iastate.edu`
4. Stop currently running server process(es) <br>
`ps -au<username>` then `kill <pid>`\
5. Remove old source and extract new build archive <br>
`unzip build-MM-DD.zip`
6. Replace the src folder with the new build
7. Reset database if schema changes were made since last build
8. Ensure database.db is writeable
9. Start the server <br>
`python run_sandbox.py &`
