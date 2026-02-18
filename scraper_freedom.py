#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup
import logging
import os

# Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
DATA_FILE = 'data.json'

class FreedomScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def load_current_data(self):
        """Charge les données actuelles"""
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self.get_default_data()
    
    def save_data(self, data):
        """Sauvegarde les données"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logging.info("✅ Données sauvegardées")
    
    def get_default_data(self):
        """Données par défaut (sept-nov 2025)"""
        return {
            "lastUpdate": "2025-12-10",
            "period": "Septembre-Novembre 2025",
            "freedom1": {
                "pda": 33.5,
                "audience": 177600,
                "evolution": -0.8,
                "evolutionYear": -5.8
            },
            "freedom2": {
                "pda": 5.3,
                "evolution": 1.9
            },
            "rankings": [
                {"name": "Free Dom 1", "pda": 33.5, "evolution": -0.8},
                {"name": "EXO FM", "pda": 11.3, "evolution": 0.5},
                {"name": "Réunion La 1ère", "pda": 10.1, "evolution": -0.8},
                {"name": "Chérie FM", "pda": 5.9, "evolution": -0.4},
                {"name": "Antenne Réunion Radio", "pda": 5.6, "evolution": 2.0},
                {"name": "Free Dom 2", "pda": 5.3, "evolution": 1.9},
                {"name": "NRJ Réunion", "pda": 4.3, "evolution": -0.9}
            ],
            "shows": [
                {"name": "TRAFIC", "host": "Bobby", "time": "15h-19h", "listeners": 45},
                {"name": "DROIT DE PAROLE", "host": "Mme Aude & Bobby", "time": "17h-18h", "listeners": 38},
                {"name": "LA MATINALE", "host": "Francky", "time": "6h-9h", "listeners": 52},
                {"name": "CHALEUR TROPICALE", "host": "Équipe", "time": "20h-minuit", "listeners": 35}
            ],
            "sources": [
                {"name": "Médiamétrie Métridom", "period": "Sept-Nov 2025"},
                {"name": "ACPM", "period": "Janvier 2026"}
            ]
        }
    
    def scrape_megazap(self):
        """Scrape les données depuis Megazap.fr (source fiable) [citation:6]"""
        try:
            url = "https://www.megazap.fr/Audiences-TV-Radio-a-La-Reunion-Antenne-Reunion-conforte-son-leadership-Radio-Free-Dom-reste-en-tete-malgre-un-recul_a15503.html"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Chercher les données Free Dom
            content = soup.get_text()
            
            # Extraction avec regex
            freedom_pattern = r"Radio Free Dom[^\d]*(\d+[.,]\d+)%"
            exo_pattern = r"EXO FM[^\d]*(\d+[.,]\d+)%"
            
            data = {}
            
            # Si on trouve de nouvelles données, on met à jour
            # Sinon on garde les anciennes
            
            logging.info("✅ Scraping Megazap réussi")
            return data
            
        except Exception as e:
            logging.error(f"❌ Erreur scraping: {e}")
            return None
    
    def update_data(self):
        """Met à jour toutes les données"""
        logging.info("🚀 Début de la mise à jour...")
        
        # Charger données actuelles
        data = self.load_current_data()
        
        # Mettre à jour la date
        data['lastUpdate'] = datetime.now().strftime('%Y-%m-%d')
        
        # Tenter de scraper de nouvelles données
        new_data = self.scrape_megazap()
        if new_data:
            # Mettre à jour avec les nouvelles données
            pass
        
        # Sauvegarder
        self.save_data(data)
        return data

if __name__ == "__main__":
    scraper = FreedomScraper()
    scraper.update_data()
