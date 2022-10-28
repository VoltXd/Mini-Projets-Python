# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 14:05:53 2022

@author: Pierre-Alexandre
"""

import sys
import matplotlib.pyplot as plt
import datetime

class Game:
    TEAM_COLOR_DICT = {"Rouge\n":'red', "Bleu\n":"blue", "Jaune\n":"yellow"}
    def __init__(self, fileName, gameTitle, location, date):
        self.players = []
        self.teams = dict()
        self.gameTitle = gameTitle
        self.location = location
        self.date = date
        try:
            f = open(fileName, 'r')
        except:
            sys.exit(-1)
            
        for line in f:
            line.strip()
            line = line.split(";")
            player = Player(int(line[0]), line[1], int(line[2]), int(line[3]), int(line[4]), line[5])
            self.AddPlayer(player)
            del player
        f.close()
        del f
        
    def AddPlayer(self, player):
        self.players.append(player)  
        if player.team not in self.teams.keys():
            self.teams[player.team] = Team(player.team)
        self.teams[player.team].AddPlayer(player)
        
    def GetTeamStats(self):
        teamsScore = dict()
        for teamName in self.teams:
            teamsScore[teamName] = 0
            for player in self.teams[teamName].players:
                teamsScore[teamName] += player.score
        
        teamsShots = dict()
        for teamName in self.teams:
            teamsShots[teamName] = 0
            for player in self.teams[teamName].players:
                teamsShots[teamName] += player.shot
        
        return teamsScore, teamsShots
    
    def PlotAllStats(self):
        #Get data
        playerNames = []
        playerScores = []
        playerShots = []
        playerRatio = []
        playerTeam = []
        playerHit = []
        playerHitScore = []
        playerRatioScore = []
        playerScoreLoss = []
        for player in self.players:
            playerNames.append(player.name)
            playerScores.append(player.score)
            playerShots.append(player.shot)
            playerRatio.append(player.ratio)
            playerTeam.append(self.TEAM_COLOR_DICT[player.team])
            playerHit.append(player.hit)
            playerHitScore.append(player.hitScore)
            playerRatioScore.append(player.ratioScore)
            playerScoreLoss.append(player.scoreLoss)
        
        teamsScore, teamsShot = self.GetTeamStats()
        
        #Plot
        plt.figure(figsize=(80,30))
        plt.suptitle("Statistiques {}\nLaser Quest {}\n{}".format(self.gameTitle, self.location, self.date.strftime("%d/%m/%Y")), fontsize=44)
        plt.subplot(331)
        plt.bar(playerNames, playerScores, color=playerTeam)        
        plt.ylabel("Score", fontsize=26)
        plt.xticks(rotation=45, fontsize=20, ha="right")
        
        plt.subplot(332)
        plt.bar(playerNames, playerShots, color=playerTeam)         
        plt.ylabel("Tirs", fontsize=26) 
        plt.xticks(rotation=45, fontsize=20, ha="right")      
        
        plt.subplot(333)
        plt.bar(playerNames, playerRatio, color=playerTeam)         
        plt.ylabel("Ratio", fontsize=26)
        plt.xticks(rotation=45, fontsize=20, ha="right")       
        
        plt.subplot(334)
        plt.bar(playerNames, playerHit, color=playerTeam)         
        plt.ylabel("Tirs Réussis", fontsize=26)       
        plt.xticks(rotation=45, fontsize=20, ha="right")
        
        plt.subplot(335)
        plt.bar(playerNames, playerHitScore, color=playerTeam)         
        plt.ylabel("Points liés aux tirs", fontsize=26)       
        plt.xticks(rotation=45, fontsize=20, ha="right")
        
        plt.subplot(336)
        plt.bar(playerNames, playerRatioScore, color=playerTeam)         
        plt.ylabel("Points liés au ratio", fontsize=26)       
        plt.xticks(rotation=45, fontsize=20, ha="right")
        
        plt.subplot(337)
        plt.bar(teamsScore.keys(), [teamsScore[k] for k in teamsScore.keys()], color=[self.TEAM_COLOR_DICT[tColor] for tColor in teamsScore.keys()])         
        plt.ylabel("Scores équipes", fontsize=26)       
        plt.xticks(rotation=45, fontsize=20, ha="right")
        plt.plot()
        
        plt.subplot(338)
        plt.bar(playerNames, playerScoreLoss, color=playerTeam)         
        plt.ylabel("Points perdus", fontsize=26)       
        plt.xticks(rotation=45, fontsize=20, ha="right")
        
        plt.subplot(339)
        plt.bar(teamsScore.keys(), [teamsScore[k] / len(self.teams[k].players) for k in teamsScore.keys()], color=[self.TEAM_COLOR_DICT[tColor] for tColor in teamsScore.keys()])         
        plt.ylabel("Scores équipes par joueurs", fontsize=26)       
        plt.xticks(rotation=45, fontsize=20, ha="right")
        plt.plot()
        
        
        plt.plot()
        plt.savefig("Lasergame_Partie1.png")
                

class Team:
    def __init__(self, name):
        self.name = name
        self.players = []
        
    def AddPlayer(self, player):
        self.players.append(player)
       

class Player:
    def __init__(self, position, name, score, shot, ratio, team):
        self.position = position
        self.name = name
        self.score = score
        self.shot = shot
        self.ratio = ratio
        self.team = team
        self.CalculateStatistics()
    
    def CalculateStatistics(self):
        self.hit = self.shot * self.ratio / 100.0
        self.hitScore = self.hit * 10.0
        self.ratioScore = self.ratio * 10 if self.ratio < 10 else 100
        self.scoreLoss = self.hitScore + self.ratioScore - self.score
        
        print(self.hit, self.hitScore, self.ratioScore, self.scoreLoss)
        return
    
    
if (__name__ == "__main__"):
    date = datetime.date(2022, 7, 7)
    game1 = Game("tableau_score_partie1.csv", "Partie 1", "Massy", date)        
        
    print(game1.GetTeamStats())
    game1.PlotAllStats()

    game2 = Game("tableau_score_partie2.csv", "Partie 2", "Massy", date)        
        
    print(game2.GetTeamStats())
    game2.PlotAllStats()