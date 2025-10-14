import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from datetime import datetime
import threading
from typing import Dict, List, Optional, Tuple
import time

class FPLStatsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FPL Stats & Team Selector")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2E3440')
        
        # Data storage
        self.players_data = []
        self.teams_data = []
        self.gameweeks_data = []
        self.current_gameweek = 1
        
        # Style configuration
        self.setup_styles()
        
        # Create main interface
        self.create_widgets()
        
        # Load initial data
        self.load_data()
    
    def setup_styles(self):
        """Configure the ttk styles for a modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       background='#2E3440', 
                       foreground='#ECEFF4', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Heading.TLabel', 
                       background='#2E3440', 
                       foreground='#88C0D0', 
                       font=('Arial', 12, 'bold'))
        
        style.configure('Custom.Treeview', 
                       background='#3B4252',
                       foreground='#ECEFF4',
                       fieldbackground='#3B4252')
        
        style.configure('Custom.TFrame', 
                       background='#2E3440')
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main title
        title_label = ttk.Label(self.root, text="FPL Stats & Team Selector", 
                               style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_overview_tab()
        self.create_players_tab()
        self.create_team_suggestion_tab()
        self.create_stats_tab()
    
    def create_overview_tab(self):
        """Create the overview tab"""
        overview_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(overview_frame, text="Overview")
        
        # Current gameweek info
        gw_frame = ttk.LabelFrame(overview_frame, text="Current Gameweek", padding=10)
        gw_frame.pack(fill='x', padx=10, pady=5)
        
        self.gw_label = ttk.Label(gw_frame, text="Loading gameweek data...", 
                                 style='Heading.TLabel')
        self.gw_label.pack()
        
        # Quick stats frame
        stats_frame = ttk.LabelFrame(overview_frame, text="Quick Stats", padding=10)
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        self.quick_stats_text = scrolledtext.ScrolledText(stats_frame, height=10, 
                                                         bg='#3B4252', fg='#ECEFF4')
        self.quick_stats_text.pack(fill='both', expand=True)
        
        # Refresh button
        refresh_btn = ttk.Button(overview_frame, text="Refresh Data", 
                               command=self.refresh_data)
        refresh_btn.pack(pady=10)
    
    def create_players_tab(self):
        """Create the players tab"""
        players_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(players_frame, text="Players")
        
        # Filter frame
        filter_frame = ttk.Frame(players_frame, style='Custom.TFrame')
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Position:", style='Heading.TLabel').pack(side='left')
        self.position_var = tk.StringVar(value="All")
        position_combo = ttk.Combobox(filter_frame, textvariable=self.position_var,
                                    values=["All", "Goalkeeper", "Defender", "Midfielder", "Forward"])
        position_combo.pack(side='left', padx=5)
        position_combo.bind('<<ComboboxSelected>>', self.filter_players)
        
        ttk.Label(filter_frame, text="Team:", style='Heading.TLabel').pack(side='left', padx=(20,0))
        self.team_var = tk.StringVar(value="All")
        self.team_combo = ttk.Combobox(filter_frame, textvariable=self.team_var)
        self.team_combo.pack(side='left', padx=5)
        self.team_combo.bind('<<ComboboxSelected>>', self.filter_players)
        
        # Players treeview
        self.players_tree = ttk.Treeview(players_frame, style='Custom.Treeview')
        self.players_tree['columns'] = ('Name', 'Team', 'Position', 'Price', 'Points', 'Form', 'Selected%')
        self.players_tree['show'] = 'headings'
        
        for col in self.players_tree['columns']:
            self.players_tree.heading(col, text=col, command=lambda c=col: self.sort_players(c))
            self.players_tree.column(col, width=120)
        
        # Scrollbar for players tree
        players_scrollbar = ttk.Scrollbar(players_frame, orient='vertical', 
                                        command=self.players_tree.yview)
        self.players_tree.configure(yscrollcommand=players_scrollbar.set)
        
        self.players_tree.pack(side='left', fill='both', expand=True, padx=(10,0), pady=5)
        players_scrollbar.pack(side='right', fill='y', padx=(0,10), pady=5)
    
    def create_team_suggestion_tab(self):
        """Create the team suggestion tab"""
        team_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(team_frame, text="Team Suggestions")
        
        # Controls frame
        controls_frame = ttk.Frame(team_frame, style='Custom.TFrame')
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(controls_frame, text="Budget (£):", style='Heading.TLabel').pack(side='left')
        self.budget_var = tk.StringVar(value="100.0")
        budget_entry = ttk.Entry(controls_frame, textvariable=self.budget_var, width=10)
        budget_entry.pack(side='left', padx=5)
        
        suggest_btn = ttk.Button(controls_frame, text="Generate Team", 
                               command=self.generate_team_suggestion)
        suggest_btn.pack(side='left', padx=20)
        
        # Team display frame
        team_display_frame = ttk.LabelFrame(team_frame, text="Suggested Team", padding=10)
        team_display_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.team_text = scrolledtext.ScrolledText(team_display_frame, height=20, 
                                                  bg='#3B4252', fg='#ECEFF4')
        self.team_text.pack(fill='both', expand=True)
    
    def create_stats_tab(self):
        """Create the statistics tab"""
        stats_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(stats_frame, text="Statistics")
        
        # Top performers frame
        top_frame = ttk.LabelFrame(stats_frame, text="Top Performers", padding=10)
        top_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.stats_text = scrolledtext.ScrolledText(top_frame, height=25, 
                                                   bg='#3B4252', fg='#ECEFF4')
        self.stats_text.pack(fill='both', expand=True)
    
    def load_data(self):
        """Load data from FPL API in a separate thread"""
        def load_thread():
            try:
                self.update_status("Loading FPL data...")
                
                # Get bootstrap data (players, teams, gameweeks)
                bootstrap_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
                response = requests.get(bootstrap_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    self.players_data = data['elements']
                    self.teams_data = data['teams']
                    self.gameweeks_data = data['events']
                    
                    # Find current gameweek
                    for gw in self.gameweeks_data:
                        if gw['is_current']:
                            self.current_gameweek = gw['id']
                            break
                    
                    # Update GUI
                    self.root.after(0, self.update_gui)
                else:
                    self.root.after(0, lambda: self.show_error(f"Failed to load data: {response.status_code}"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.show_error(f"Error loading data: {str(e)}"))
        
        thread = threading.Thread(target=load_thread)
        thread.daemon = True
        thread.start()
    
    def update_gui(self):
        """Update all GUI elements with loaded data"""
        self.update_gameweek_info()
        self.populate_players_tree()
        self.update_team_combo()
        self.update_quick_stats()
        self.update_statistics()
        self.update_status("Data loaded successfully!")
    
    def update_gameweek_info(self):
        """Update gameweek information"""
        current_gw = next((gw for gw in self.gameweeks_data if gw['id'] == self.current_gameweek), None)
        if current_gw:
            self.gw_label.config(text=f"Gameweek {current_gw['id']}: {current_gw['name']}")
    
    def populate_players_tree(self):
        """Populate the players treeview"""
        # Clear existing items
        for item in self.players_tree.get_children():
            self.players_tree.delete(item)
        
        # Get team names mapping
        team_names = {team['id']: team['name'] for team in self.teams_data}
        position_names = {1: 'Goalkeeper', 2: 'Defender', 3: 'Midfielder', 4: 'Forward'}
        
        # Add players
        for player in self.players_data:
            if player['status'] not in ['i', 'u']:  # Only available players
                team_name = team_names.get(player['team'], 'Unknown')
                position_name = position_names.get(player['element_type'], 'Unknown')
                price = f"£{player['now_cost'] / 10:.1f}m"
                
                self.players_tree.insert('', 'end', values=(
                    player['web_name'],
                    team_name,
                    position_name,
                    price,
                    player['total_points'],
                    player['form'],
                    f"{player['selected_by_percent']}%"
                ))
    
    def update_team_combo(self):
        """Update team combo box with team names"""
        team_names = ["All"] + [team['name'] for team in self.teams_data]
        self.team_combo['values'] = team_names
    
    def update_quick_stats(self):
        """Update quick stats display"""
        if not self.players_data:
            return
        
        stats_text = "=== QUICK FPL STATISTICS ===\n\n"
        
        # Most expensive players
        expensive_players = sorted(self.players_data, key=lambda x: x['now_cost'], reverse=True)[:5]
        stats_text += "🔸 Most Expensive Players:\n"
        for player in expensive_players:
            stats_text += f"  • {player['web_name']}: £{player['now_cost']/10:.1f}m\n"
        
        # Highest scoring players
        stats_text += "\n🔸 Highest Scoring Players:\n"
        top_scorers = sorted(self.players_data, key=lambda x: x['total_points'], reverse=True)[:5]
        for player in top_scorers:
            stats_text += f"  • {player['web_name']}: {player['total_points']} points\n"
        
        # Best form players
        stats_text += "\n🔸 Best Form Players (last 5 games):\n"
        in_form = sorted([p for p in self.players_data if p['form'] != '0.0'], 
                        key=lambda x: float(x['form']), reverse=True)[:5]
        for player in in_form:
            stats_text += f"  • {player['web_name']}: {player['form']} avg\n"
        
        # Most selected players
        stats_text += "\n🔸 Most Selected Players:\n"
        popular = sorted(self.players_data, key=lambda x: float(x['selected_by_percent']), reverse=True)[:5]
        for player in popular:
            stats_text += f"  • {player['web_name']}: {player['selected_by_percent']}%\n"
        
        self.quick_stats_text.delete(1.0, tk.END)
        self.quick_stats_text.insert(1.0, stats_text)
    
    def update_statistics(self):
        """Update detailed statistics"""
        if not self.players_data:
            return
        
        stats_text = "=== DETAILED FPL STATISTICS ===\n\n"
        
        # Position analysis
        position_names = {1: 'Goalkeeper', 2: 'Defender', 3: 'Midfielder', 4: 'Forward'}
        for pos_id, pos_name in position_names.items():
            players_in_pos = [p for p in self.players_data if p['element_type'] == pos_id]
            if not players_in_pos:
                continue
                
            stats_text += f"📊 {pos_name.upper()} ANALYSIS:\n"
            
            # Top scorers in position
            top_in_pos = sorted(players_in_pos, key=lambda x: x['total_points'], reverse=True)[:3]
            stats_text += "  Top Scorers:\n"
            for player in top_in_pos:
                stats_text += f"    • {player['web_name']}: {player['total_points']} pts (£{player['now_cost']/10:.1f}m)\n"
            
            # Best value in position (points per million)
            value_in_pos = sorted(players_in_pos, 
                                key=lambda x: x['total_points'] / (x['now_cost']/10) if x['now_cost'] > 0 else 0, 
                                reverse=True)[:3]
            stats_text += "  Best Value:\n"
            for player in value_in_pos:
                ppm = player['total_points'] / (player['now_cost']/10) if player['now_cost'] > 0 else 0
                stats_text += f"    • {player['web_name']}: {ppm:.1f} pts/£m\n"
            
            stats_text += "\n"
        
        # Team analysis
        stats_text += "🏆 TEAM ANALYSIS:\n"
        team_stats = {}
        for team in self.teams_data:
            team_players = [p for p in self.players_data if p['team'] == team['id']]
            total_points = sum(p['total_points'] for p in team_players)
            team_stats[team['name']] = total_points
        
        sorted_teams = sorted(team_stats.items(), key=lambda x: x[1], reverse=True)
        stats_text += "  Total Points by Team:\n"
        for team_name, points in sorted_teams[:10]:
            stats_text += f"    • {team_name}: {points} points\n"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
    
    def filter_players(self, event=None):
        """Filter players based on position and team selection"""
        # Clear existing items
        for item in self.players_tree.get_children():
            self.players_tree.delete(item)
        
        position_filter = self.position_var.get()
        team_filter = self.team_var.get()
        
        # Get mappings
        team_names = {team['id']: team['name'] for team in self.teams_data}
        position_names = {1: 'Goalkeeper', 2: 'Defender', 3: 'Midfielder', 4: 'Forward'}
        position_ids = {v: k for k, v in position_names.items()}
        
        for player in self.players_data:
            if player['status'] in ['i', 'u']:  # Skip unavailable players
                continue
            
            # Apply filters
            if position_filter != "All":
                if player['element_type'] != position_ids[position_filter]:
                    continue
            
            if team_filter != "All":
                if team_names.get(player['team']) != team_filter:
                    continue
            
            team_name = team_names.get(player['team'], 'Unknown')
            position_name = position_names.get(player['element_type'], 'Unknown')
            price = f"£{player['now_cost'] / 10:.1f}m"
            
            self.players_tree.insert('', 'end', values=(
                player['web_name'],
                team_name,
                position_name,
                price,
                player['total_points'],
                player['form'],
                f"{player['selected_by_percent']}%"
            ))
    
    def sort_players(self, column):
        """Sort players by selected column"""
        items = [(self.players_tree.set(child, column), child) for child in self.players_tree.get_children()]
        
        # Determine if we should sort numerically
        numeric_columns = ['Price', 'Points', 'Form', 'Selected%']
        if column in numeric_columns:
            try:
                items.sort(key=lambda x: float(x[0].replace('£', '').replace('m', '').replace('%', '')), reverse=True)
            except:
                items.sort(reverse=True)
        else:
            items.sort()
        
        # Rearrange items
        for index, (val, child) in enumerate(items):
            self.players_tree.move(child, '', index)
    
    def generate_team_suggestion(self):
        """Generate an optimal team suggestion based on form and value"""
        try:
            budget = float(self.budget_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid budget")
            return
        
        if not self.players_data:
            messagebox.showerror("Error", "No player data available")
            return
        
        self.team_text.delete(1.0, tk.END)
        self.team_text.insert(tk.END, "Generating optimal team...\n\n")
        self.root.update()
        
        # Filter available players
        available_players = [p for p in self.players_data if p['status'] not in ['i', 'u']]
        
        # Sort players by form and points per million
        for player in available_players:
            player['value_score'] = (
                player['total_points'] * 0.4 +
                float(player['form']) * 30 * 0.4 +
                (100 - float(player['selected_by_percent'])) * 0.2
            ) / (player['now_cost'] / 10)
        
        # Generate team
        team = self.select_optimal_team(available_players, budget)
        
        if team:
            self.display_suggested_team(team)
        else:
            self.team_text.insert(tk.END, "Could not generate a valid team within budget constraints.")
    
    def select_optimal_team(self, players, budget):
        """Select optimal team using a greedy approach"""
        # Separate by position
        gks = [p for p in players if p['element_type'] == 1]
        defs = [p for p in players if p['element_type'] == 2]
        mids = [p for p in players if p['element_type'] == 3]
        fwds = [p for p in players if p['element_type'] == 4]
        
        # Sort by value score
        gks.sort(key=lambda x: x['value_score'], reverse=True)
        defs.sort(key=lambda x: x['value_score'], reverse=True)
        mids.sort(key=lambda x: x['value_score'], reverse=True)
        fwds.sort(key=lambda x: x['value_score'], reverse=True)
        
        # Try different formations
        formations = [
            (2, 5, 5, 3),  # 2-5-5-3
            (2, 5, 4, 4),  # 2-5-4-4
            (2, 4, 5, 4),  # 2-4-5-4
        ]
        
        best_team = None
        best_score = 0
        
        for formation in formations:
            gk_count, def_count, mid_count, fwd_count = formation
            team = self.try_formation(gks, defs, mids, fwds, 
                                    gk_count, def_count, mid_count, fwd_count, budget)
            if team:
                team_score = sum(p['value_score'] for p in team)
                if team_score > best_score:
                    best_score = team_score
                    best_team = team
        
        return best_team
    
    def try_formation(self, gks, defs, mids, fwds, gk_count, def_count, mid_count, fwd_count, budget):
        """Try to build a team with specific formation"""
        team = []
        current_budget = budget
        
        # Select players for each position
        positions = [
            (gks, gk_count),
            (defs, def_count),
            (mids, mid_count),
            (fwds, fwd_count)
        ]
        
        for position_players, count in positions:
            selected_teams = set()
            position_team = []
            
            for player in position_players:
                if len(position_team) >= count:
                    break
                
                player_cost = player['now_cost'] / 10
                if player_cost <= current_budget and player['team'] not in selected_teams:
                    position_team.append(player)
                    current_budget -= player_cost
                    selected_teams.add(player['team'])
            
            if len(position_team) < count:
                return None  # Couldn't fill position
            
            team.extend(position_team)
        
        return team if len(team) == 15 else None
    
    def display_suggested_team(self, team):
        """Display the suggested team"""
        self.team_text.delete(1.0, tk.END)
        
        # Get team names and position names
        team_names = {team_data['id']: team_data['name'] for team_data in self.teams_data}
        position_names = {1: 'Goalkeeper', 2: 'Defender', 3: 'Midfielder', 4: 'Forward'}
        
        total_cost = sum(p['now_cost'] / 10 for p in team)
        total_points = sum(p['total_points'] for p in team)
        avg_form = sum(float(p['form']) for p in team) / len(team)
        
        output = f"🏆 SUGGESTED TEAM OF THE WEEK 🏆\n"
        output += f"{'='*50}\n\n"
        output += f"💰 Total Cost: £{total_cost:.1f}m\n"
        output += f"⚽ Total Points: {total_points}\n"
        output += f"📈 Average Form: {avg_form:.2f}\n\n"
        
        # Group by position
        by_position = {}
        for player in team:
            pos = position_names[player['element_type']]
            if pos not in by_position:
                by_position[pos] = []
            by_position[pos].append(player)
        
        # Display by position
        for position in ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']:
            if position in by_position:
                output += f"🔸 {position.upper()}S:\n"
                for player in by_position[position]:
                    team_name = team_names.get(player['team'], 'Unknown')
                    output += f"  • {player['web_name']} ({team_name})\n"
                    output += f"    Price: £{player['now_cost']/10:.1f}m | Points: {player['total_points']} | Form: {player['form']}\n"
                output += "\n"
        
        # Additional insights
        output += "📊 TEAM INSIGHTS:\n"
        output += f"• Most expensive player: {max(team, key=lambda x: x['now_cost'])['web_name']} (£{max(team, key=lambda x: x['now_cost'])['now_cost']/10:.1f}m)\n"
        output += f"• Highest scorer: {max(team, key=lambda x: x['total_points'])['web_name']} ({max(team, key=lambda x: x['total_points'])['total_points']} pts)\n"
        output += f"• Best form: {max(team, key=lambda x: float(x['form']))['web_name']} ({max(team, key=lambda x: float(x['form']))['form']})\n"
        
        # Team distribution
        team_distribution = {}
        for player in team:
            team_name = team_names.get(player['team'], 'Unknown')
            team_distribution[team_name] = team_distribution.get(team_name, 0) + 1
        
        output += f"\n🏟️ TEAM DISTRIBUTION:\n"
        for team_name, count in sorted(team_distribution.items(), key=lambda x: x[1], reverse=True):
            output += f"• {team_name}: {count} player{'s' if count > 1 else ''}\n"
        
        self.team_text.insert(1.0, output)
    
    def refresh_data(self):
        """Refresh all data from the API"""
        self.load_data()
    
    def update_status(self, message):
        """Update status (could be implemented as a status bar)"""
        print(f"Status: {message}")  # For now, just print to console
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = FPLStatsGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()