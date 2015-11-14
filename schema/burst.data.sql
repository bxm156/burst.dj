PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE playlist (
	id INTEGER NOT NULL, 
	time_created DATETIME, 
	name VARCHAR, 
	user_id INTEGER, 
	tracks TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO "playlist" VALUES(1,'2015-11-13 22:44:53','scandinavia',1,'[3, 4, 5, 6, 1, 2, 61]');
INSERT INTO "playlist" VALUES(2,'2015-11-13 22:49:00','songs',3,'[9, 7, 8]');
INSERT INTO "playlist" VALUES(3,'2015-11-13 23:09:14','Hack List',2,'[12, 13, 10, 11]');
INSERT INTO "playlist" VALUES(4,'2015-11-13 23:12:00','ratchet',1,'[14, 15, 16, 17, 18, 59, 20]');
INSERT INTO "playlist" VALUES(5,'2015-11-13 23:19:51','two steps from hell',5,'[21]');
INSERT INTO "playlist" VALUES(6,'2015-11-13 23:20:09','west coast hip hop',3,'[26, 22, 23, 24, 25]');
INSERT INTO "playlist" VALUES(7,'2015-11-13 23:23:01','deez',6,'[27, 28, 29]');
INSERT INTO "playlist" VALUES(8,'2015-11-13 23:26:43','deez2',6,'[29]');
INSERT INTO "playlist" VALUES(9,'2015-11-13 23:38:48','eminem',5,'[31, 30]');
INSERT INTO "playlist" VALUES(10,'2015-11-13 23:53:35','pop',3,'[32]');
INSERT INTO "playlist" VALUES(11,'2015-11-13 23:54:33','Hackathon 18',2,'[48, 12, 33, 34, 1, 62, 41, 42, 43, 45, 46, 47]');
INSERT INTO "playlist" VALUES(12,'2015-11-13 23:55:31','pop pop',3,'[36, 37, 38, 39, 63, 40, 44, 32, 35]');
INSERT INTO "playlist" VALUES(13,'2015-11-14 00:00:10','rock',3,'[49, 50, 51, 52, 53, 54, 55, 56]');
INSERT INTO "playlist" VALUES(14,'2015-11-14 00:07:38','Hackathon 18 -3',2,'[57]');
INSERT INTO "playlist" VALUES(15,'2015-11-14 00:12:22','hack',3,'[58]');
INSERT INTO "playlist" VALUES(16,'2015-11-14 00:22:17','huhhack',3,'[60]');
INSERT INTO "playlist" VALUES(17,'2015-11-14 01:18:15','space jam',3,'[64]');
INSERT INTO "playlist" VALUES(18,'2015-11-14 01:30:47','sweater wheater',1,'[66, 67, 68, 65]');
INSERT INTO "playlist" VALUES(19,'2015-11-14 01:32:29','deep house',3,'[69, 70, 71]');
INSERT INTO "playlist" VALUES(20,'2015-11-14 01:37:38','other',2,'[72]');
INSERT INTO "playlist" VALUES(21,'2015-11-14 20:32:31','deez',4,'[73]');
CREATE TABLE room_user (
	time_created DATETIME, 
	room_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	last_ping_time DATETIME, 
	PRIMARY KEY (room_id, user_id), 
	FOREIGN KEY(room_id) REFERENCES room (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO "room_user" VALUES('2015-11-13 23:05:33',1,4,'2015-11-13 23:05:33');
INSERT INTO "room_user" VALUES('2015-11-13 23:16:45',1,5,'2015-11-13 23:16:45');
INSERT INTO "room_user" VALUES('2015-11-13 23:22:57',1,6,'2015-11-13 23:22:57');
INSERT INTO "room_user" VALUES('2015-11-13 23:23:30',1,3,'2015-11-13 23:23:30');
INSERT INTO "room_user" VALUES('2015-11-13 23:30:41',1,1,'2015-11-13 23:30:41');
INSERT INTO "room_user" VALUES('2015-11-13 23:30:59',1,2,'2015-11-13 23:30:59');
CREATE TABLE room (
	id INTEGER NOT NULL, 
	time_created DATETIME, 
	name VARCHAR, 
	current_user_id INTEGER, 
	current_track_id INTEGER, 
	time_track_started DATETIME, 
	time_scrubbed DATETIME, 
	admin_user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(current_user_id) REFERENCES user (id)
);
INSERT INTO "room" VALUES(1,'2015-11-13 22:41:13','Club Six',1,20,'2015-11-14 12:57:02.859876','2015-11-13 22:41:13',1);
CREATE TABLE track (
	id INTEGER NOT NULL, 
	time_created DATETIME, 
	name VARCHAR, 
	provider INTEGER, 
	provider_track_id VARCHAR, 
	length INTEGER, 
	average_rating INTEGER, 
	PRIMARY KEY (id)
);
INSERT INTO "track" VALUES(1,'2015-11-13 22:45:01','Ace of Base - The Sign (Official Music Video)','youtube','iqu132vTl5Y',199,NULL);
INSERT INTO "track" VALUES(2,'2015-11-13 22:45:04','Ace of Base -  Don''t Turn Around (Official Music Video)','youtube','B_gs4gCyGKs',233,NULL);
INSERT INTO "track" VALUES(3,'2015-11-13 22:45:05','Ace of Base - All That She Wants (Official Music Video)','youtube','d73tiBBzvFM',214,NULL);
INSERT INTO "track" VALUES(4,'2015-11-13 22:45:07','Ace of Base - Happy Nation (Official Music Video)','youtube','HWjCStB6k4o',213,NULL);
INSERT INTO "track" VALUES(5,'2015-11-13 22:45:11','Ace of Base - Never Gonna Say I''m Sorry (Official)','youtube','Lm12gDg0D8c',196,NULL);
INSERT INTO "track" VALUES(6,'2015-11-13 22:45:13','Ace of Base - Beautiful Life (Official Music Video)','youtube','wh-07BzfgYY',223,NULL);
INSERT INTO "track" VALUES(7,'2015-11-13 22:49:07','Santigold - Disparate Youth [Official Music Video]','youtube','mIMMZQJ1H6E',240,NULL);
INSERT INTO "track" VALUES(8,'2015-11-13 22:49:09','Santigold - Shove It','youtube','Ez2wYCRjYyY',227,NULL);
INSERT INTO "track" VALUES(9,'2015-11-13 22:49:34','[Electro] - Pegboard Nerds - Disconnected [Monstercat Release]','youtube','MwSkC85TDgY',243,NULL);
INSERT INTO "track" VALUES(10,'2015-11-13 23:09:53','Harlem Shake - Yelp SF','youtube','5WSHHJfLHYw',31,NULL);
INSERT INTO "track" VALUES(11,'2015-11-13 23:10:04','Harlem Shake - Yelp London','youtube','aqt8QiYDixs',31,NULL);
INSERT INTO "track" VALUES(12,'2015-11-13 23:10:04','Yelp NYC Harlem Shake','youtube','0SImtGLhOHM',87,NULL);
INSERT INTO "track" VALUES(13,'2015-11-13 23:10:06','Harlem Shake - Yelp Edition (PHX)','youtube','M-NgGDlr7uo',30,NULL);
INSERT INTO "track" VALUES(14,'2015-11-13 23:12:13','Tinashe - 2 On (Explicit) ft. SchoolBoy Q','youtube','-s7TCuCpB5c',231,NULL);
INSERT INTO "track" VALUES(15,'2015-11-13 23:12:26','Drake - The Motto (Explicit) ft. Lil Wayne, Tyga','youtube','BYDKK95cpfM',243,NULL);
INSERT INTO "track" VALUES(16,'2015-11-13 23:13:06','Beyoncé - 7/11','youtube','k4YRWT_Aldo',217,NULL);
INSERT INTO "track" VALUES(17,'2015-11-13 23:13:36','Drake - Hotline Bling','youtube','uxpDa-c-4Mc',296,NULL);
INSERT INTO "track" VALUES(18,'2015-11-13 23:13:50','Rae Sremmurd - No Flex Zone (Explicit)','youtube','p2cQSPRTdhg',289,NULL);
INSERT INTO "track" VALUES(19,'2015-11-13 23:14:16','Nicki Minaj Truffle Butter Ft. Drake,Lil Wayne (Official Video)','youtube','Pzqe-yJWmLk',215,NULL);
INSERT INTO "track" VALUES(20,'2015-11-13 23:14:28','Big Sean - I Don''t Fuck With You (Explicit) ft. E-40','youtube','cZaJYDPY-YQ',348,NULL);
INSERT INTO "track" VALUES(21,'2015-11-13 23:20:01','Epic Battle Music: Dragon Rider','youtube','k-2IT8rcdj0',110,NULL);
INSERT INTO "track" VALUES(22,'2015-11-13 23:20:23','Dr. Dre - Still D.R.E. ft. Snoop Dogg','youtube','_CL6n0FJZpk',292,NULL);
INSERT INTO "track" VALUES(23,'2015-11-13 23:20:32','Tupac-Changes','youtube','vL5sdu3pNrU',270,NULL);
INSERT INTO "track" VALUES(24,'2015-11-13 23:21:51','snoop doggy dogg - who am I ( what''s my name?)','youtube','UbI2TS0fW4Q',247,NULL);
INSERT INTO "track" VALUES(25,'2015-11-13 23:22:17','Warren G - Regulate ft. Nate Dogg','youtube','1plPyJdXKIY',240,NULL);
INSERT INTO "track" VALUES(26,'2015-11-13 23:22:41','Ice Cube - Today Was A Good Day','youtube','8CPlF-IEkXQ',261,NULL);
INSERT INTO "track" VALUES(27,'2015-11-13 23:23:11','Deez Nuts Vine Compilation | Deez Nuts Got em Vines','youtube','VcnUTyI9iJU',717,NULL);
INSERT INTO "track" VALUES(28,'2015-11-13 23:23:22','TOP KEK.mp4','youtube','6hcSpSC8T0M',7,NULL);
INSERT INTO "track" VALUES(29,'2015-11-13 23:23:28','Watch your profanity','youtube','hpigjnKl7nI',7,NULL);
INSERT INTO "track" VALUES(30,'2015-11-13 23:38:57','Eminem - Lose Yourself [HD]','youtube','_Yhyp-_hX2s',324,NULL);
INSERT INTO "track" VALUES(31,'2015-11-13 23:39:10','Eminem - Without Me','youtube','YVkUvmDQ3HY',300,NULL);
INSERT INTO "track" VALUES(32,'2015-11-13 23:53:53','Taylor Swift - Style','youtube','-CmadmM5cOk',243,NULL);
INSERT INTO "track" VALUES(33,'2015-11-13 23:55:22','Rihanna - Umbrella (Orange Version) ft. JAY-Z','youtube','CvBfHwUxHIk',254,NULL);
INSERT INTO "track" VALUES(34,'2015-11-13 23:55:38','Lost Woods Dubstep Remix - Ephixa (Download at www.ephixa.com Zelda Step)','youtube','NU75uz0b8EU',234,NULL);
INSERT INTO "track" VALUES(35,'2015-11-13 23:55:47','Backstreet Boys - I Want It That Way','youtube','4fndeDfaWCg',220,NULL);
INSERT INTO "track" VALUES(36,'2015-11-13 23:55:54','Christina Aguilera - Genie In A Bottle','youtube','kIDWgqDBNXA',217,NULL);
INSERT INTO "track" VALUES(37,'2015-11-13 23:56:03','Britney Spears - ...Baby One More Time','youtube','C-u5WLJ9Yk4',237,NULL);
INSERT INTO "track" VALUES(38,'2015-11-13 23:56:17','TLC - No Scrubs','youtube','FrLequ6dUdM',250,NULL);
INSERT INTO "track" VALUES(39,'2015-11-13 23:56:24','''N Sync - It''s Gonna Be Me (Official Video)','youtube','GQMlWwIXg3M',204,NULL);
INSERT INTO "track" VALUES(40,'2015-11-13 23:56:39','Vanessa Carlton - A Thousand Miles','youtube','Cwkej79U3ek',269,NULL);
INSERT INTO "track" VALUES(41,'2015-11-13 23:56:54','Ke$ha - Blow','youtube','CFWX0hWCbng',254,NULL);
INSERT INTO "track" VALUES(42,'2015-11-13 23:57:05','Lady Gaga - Bad Romance','youtube','qrO4YZeyl0I',308,NULL);
INSERT INTO "track" VALUES(43,'2015-11-13 23:57:46','FROZEN - Let It Go Sing-along | Official Disney HD','youtube','L0MK7qz13bU',243,NULL);
INSERT INTO "track" VALUES(44,'2015-11-13 23:57:47','One Direction - What Makes You Beautiful','youtube','QJO3ROT-A4E',207,NULL);
INSERT INTO "track" VALUES(45,'2015-11-13 23:59:35','Britney Spears - Work B**ch','youtube','pt8VYOfr8To',235,NULL);
INSERT INTO "track" VALUES(46,'2015-11-13 23:59:45','Mulan - i''ll make a man out of you','youtube','ZSS5dEeMX64',203,NULL);
INSERT INTO "track" VALUES(47,'2015-11-14 00:00:02','Darude - Sandstorm','youtube','y6120QOlsfU',233,NULL);
INSERT INTO "track" VALUES(48,'2015-11-14 00:00:07','Rick Astley - Never Gonna Give You Up','youtube','dQw4w9WgXcQ',213,NULL);
INSERT INTO "track" VALUES(49,'2015-11-14 00:00:16','The Strokes - Reptilia','youtube','b8-tXG8KrWs',215,NULL);
INSERT INTO "track" VALUES(50,'2015-11-14 00:00:27','Red Hot Chili Peppers - Californication [Official Music Video]','youtube','YlUKcNNmywk',322,NULL);
INSERT INTO "track" VALUES(51,'2015-11-14 00:00:38','Smashing Pumpkins - 1979','youtube','Lr58WHo2ndM',266,NULL);
INSERT INTO "track" VALUES(52,'2015-11-14 00:01:23','Nirvana - Come As You Are','youtube','vabnZ9-ex7o',226,NULL);
INSERT INTO "track" VALUES(53,'2015-11-14 00:01:32','Muse - Uprising','youtube','w8KQmps-Sog',252,NULL);
INSERT INTO "track" VALUES(54,'2015-11-14 00:02:03','Arctic Monkeys - Do I Wanna Know? (Official Video)','youtube','bpOSxM0rNPM',266,NULL);
INSERT INTO "track" VALUES(55,'2015-11-14 00:02:32','The Black Keys - Lonely Boy [Official Music Video]','youtube','a_426RiwST8',196,NULL);
INSERT INTO "track" VALUES(56,'2015-11-14 00:02:56','The Killers - Mr. Brightside','youtube','gGdGFtwCNBE',228,NULL);
INSERT INTO "track" VALUES(57,'2015-11-14 00:07:56','I''m On A Boat (ft. T-Pain) - Album Version','youtube','R7yfISlGLNU',189,NULL);
INSERT INTO "track" VALUES(58,'2015-11-14 00:12:42','Justin Bieber - Sorry (Dance Video)','youtube','fRh_vgS2dFE',206,NULL);
INSERT INTO "track" VALUES(59,'2015-11-14 00:13:32','DJ Snake & AlunaGeorge - You Know You Like It','youtube','aBn7bjy9c4U',273,NULL);
INSERT INTO "track" VALUES(60,'2015-11-14 00:22:23','Justin Bieber Carpool Karaoke','youtube','Dx06c0ZEBMk',497,NULL);
INSERT INTO "track" VALUES(61,'2015-11-14 00:45:00','Abba - The Winner Takes It All','youtube','92cwKCU8Z5c',296,NULL);
INSERT INTO "track" VALUES(62,'2015-11-14 00:45:50','M83 ''Midnight City'' Official video','youtube','dX3k_QDnzHE',244,NULL);
INSERT INTO "track" VALUES(63,'2015-11-14 00:57:43','Justin Bieber - Sorry (Lyric Video)','youtube','8ELbX5CMomE',199,NULL);
INSERT INTO "track" VALUES(64,'2015-11-14 01:18:29','Space Jam Theme Song','youtube','J9FImc2LOr8',251,NULL);
INSERT INTO "track" VALUES(65,'2015-11-14 01:30:56','ABBA greatest hits full album','youtube','C9IVx4lk7Ro',4581,NULL);
INSERT INTO "track" VALUES(66,'2015-11-14 01:31:20','Abba - Dancing Queen','youtube','xFrGuyw1V8s',232,NULL);
INSERT INTO "track" VALUES(67,'2015-11-14 01:31:25','Delia - Da, mama (by Carla''s Dreams) Official Video','youtube','_PYSqcyUIYQ',252,NULL);
INSERT INTO "track" VALUES(68,'2015-11-14 01:31:46','50 Cent - In Da Club (Int''l Version)','youtube','5qm8PH4xAss',250,NULL);
INSERT INTO "track" VALUES(69,'2015-11-14 01:32:45','Kaskade | Disarm You ft Ilsey (Official Audio)','youtube','3qen7he4Y7c',242,NULL);
INSERT INTO "track" VALUES(70,'2015-11-14 01:32:51','Kaskade - Atmosphere (Official Video)','youtube','sXQVicNodMw',254,NULL);
INSERT INTO "track" VALUES(71,'2015-11-14 01:32:54','Kaskade | Ultra Music Festival 2014 (Live)','youtube','6A7UMUaXIxI',3413,NULL);
INSERT INTO "track" VALUES(72,'2015-11-14 01:37:48','Dancing Queen!','youtube','TGfNSitVQFM',197,NULL);
INSERT INTO "track" VALUES(73,'2015-11-14 20:35:47','Drake - Hotline Bling','YOUTUBE','uxpDa-c-4Mc',296,NULL);
CREATE TABLE user_track_rating (
	id INTEGER NOT NULL, 
	time_created DATETIME, 
	user_id INTEGER, 
	track_id INTEGER, 
	rating INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(track_id) REFERENCES track (id)
);
CREATE TABLE room_queue (
	time_created DATETIME, 
	room_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (room_id, user_id), 
	FOREIGN KEY(room_id) REFERENCES room (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
INSERT INTO "room_queue" VALUES(NULL,1,3);
INSERT INTO "room_queue" VALUES(NULL,1,1);
CREATE TABLE user (
	id INTEGER NOT NULL, 
	time_created DATETIME, 
	name VARCHAR, 
	avatar_url VARCHAR, 
	active_playlist_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(active_playlist_id) REFERENCES playlist (id)
);
INSERT INTO "user" VALUES(1,'2015-11-13 22:38:16','jcontemp',NULL,4);
INSERT INTO "user" VALUES(2,'2015-11-13 22:46:08','bmarty',NULL,20);
INSERT INTO "user" VALUES(3,'2015-11-13 22:46:14','ptiet',NULL,12);
INSERT INTO "user" VALUES(4,'2015-11-13 22:53:21','mulan',NULL,21);
INSERT INTO "user" VALUES(5,'2015-11-13 23:16:44','aibek',NULL,9);
INSERT INTO "user" VALUES(6,'2015-11-13 23:21:44','rroeder',NULL,8);
CREATE TABLE room_queue_lock (
	time_created DATETIME,
	room_id INTEGER NOT NULL,
	PRIMARY KEY (room_id)
);
CREATE UNIQUE INDEX room_name ON room (name);
CREATE UNIQUE INDEX track_id ON track (provider, provider_track_id);
CREATE UNIQUE INDEX user_name ON user (name);
COMMIT;
