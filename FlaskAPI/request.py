import requests 


pgn_str = '[Event "Live Chess"][Site "Chess.com"][Date "2021.07.30"][Round "?"][White "michel"][Black "martinovichev"][Result "1-0"][ECO "D10"][WhiteElo "1050"][BlackElo "1018"][TimeControl "300+5"][EndTime "12:10:02 PDT"][Termination "michel won by resignation"]1. d4 d5 2. c4 c6 3. Nc3 Nf6 4. Nf3 Bg4 5. e3 e6 6. h3 Bh5 7. Be2 Bb4 8. O-O Ne4 9. Nxe4 dxe4 10. Ne5 Bxe2 11. Qxe2 Nd7 12. a3 Bd6 13. Qg4 Nxe5 14. dxe5 Bxe5 15. Rd1 Qc7 16. Qxe4 O-O 17. f4 Bf6 18. g4 Rfd8 19. Rxd8+ Rxd8 20. Qf3 Rd3 21. g5 Bd4 22. Qe2 Qxf4 23. Qxd3 Qg3+ 24. Kf1 Qxh3+ 25. Ke1 Qg3+ 26. Kd2 Bb6 27. c5 Ba5+ 28. b4 Bc7 29. Bb2 Qxg5 30. Qd7 Qg2+ 31. Kd3 Qd5+ 32. Qxd5 cxd5 33. Rc1 Kf8 34. c6 b6 35. Kd4 g5 36. a4 h5 37. Rh1 h4 38. Bc1 Kg7 39. e4 Kf6 40. exd5 exd5 41. Kxd5 Kf5 42. Rf1+ Kg6 43. Bxg5 Kxg5 44. Rxf7 Bf4 45. c7 Bxc7 46. Rxc7 h3 47. Rh7 Kg4 48. Kc6 Kg3 49. Kb7 h2 50. Kxa7 Kg2 51. Kxb6 h1=Q 52. Rxh1 Kxh1 53. a5 Kg2 54. a6 Kf3 55. a7 Ke4 56. a8=Q+ Kd3 57. Ka5 Kc4 58. b5 Kb3 59. b6 Kc4 60. b7 Kc5 61. b8=Q Kc4 62. Qc6+ Kd4 63. Qbd6+ Ke3 64. Qe8+ Kf2 65. Qdf8+ Kg3 66. Qg6+ 1-0'

pgn = '[Event "Live Chess"][Site "Chess.com"][Date "2021.08.09"][Round "?"][White "bw713"][Black "martinovichev"][Result "0-1"][ECO "B01"][WhiteElo "1009"][BlackElo "1048"][TimeControl "300+5"][EndTime "14:56:24 PDT"][Termination "martinovichev won by resignation"]1. e4 d5 2. exd5 Nf6 3. d4 Qxd5 4. Nc3 Qd6 5. Nf3 Nc6 6. Be2 Bf5 7. Bd3 Bg6 8. Bxg6 hxg6 9. Be3 e6 10. Qd2 O-O-O 11. O-O-O Nd5 12. Bf4 e5 13. Bg3 Nxc3 14. Qxc3 Nxd4 15. Nxd4 exd4 16. Rxd4 Qxd4 17. Bd6 Rxd6 0-1'

URL = 'http://127.0.0.1:5000/predict'
headers = {"Content-Type": "application/json"}
data = {"input": pgn_str}

r = requests.get(URL,headers=headers, json=data) 

print(r.json())