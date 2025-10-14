# FPL Stats & Team Selector

A comprehensive GUI application for Fantasy Premier League (FPL) that displays player statistics and suggests optimal teams based on current form and value.

## Features

- **Overview Tab**: Current gameweek information and quick statistics
- **Players Tab**: Searchable and sortable player database with filters
- **Team Suggestions**: AI-generated optimal team recommendations
- **Statistics Tab**: Detailed performance analysis by position and team

## Key Functionality

### 🏆 Team Suggestions
- Generates optimal 15-player teams within budget constraints
- Considers multiple factors:
  - Total points scored
  - Current form (last 5 games)
  - Player ownership percentage
  - Value for money (points per million)
- Tries multiple formations (2-5-5-3, 2-5-4-4, 2-4-5-4)
- Ensures team diversity (max 3 players from same team)

### 📊 Player Analysis
- Filter by position (GK, DEF, MID, FWD)
- Filter by team
- Sort by any column (price, points, form, selection %)
- Real-time data from official FPL API

### 📈 Statistics
- Top performers by position
- Best value players (points per million)
- Team analysis and total points
- Form analysis and trending players

## Installation

1. Install Python 3.7+ if not already installed
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python fpl_gui.py
```

## Data Source

The application uses the official Fantasy Premier League API:
- Base URL: `https://fantasy.premierleague.com/api/bootstrap-static/`
- Updates automatically with current gameweek data
- Includes all player statistics, team information, and gameweek details

## GUI Features

- **Modern Dark Theme**: Easy on the eyes with Nord color scheme
- **Tabbed Interface**: Organized sections for different functions
- **Real-time Updates**: Refresh button to get latest data
- **Responsive Design**: Resizable windows and scrollable content
- **Error Handling**: Graceful handling of network issues and API errors

## Team Selection Algorithm

The team suggestion algorithm uses a weighted scoring system:
- **40%** Total points scored this season
- **40%** Current form (average points last 5 games)
- **20%** Inverse ownership percentage (finding hidden gems)

The score is then divided by player price to get value score, ensuring budget-conscious selections.

## Requirements

- Python 3.7+
- tkinter (usually comes with Python)
- requests library
- Internet connection for API access

## Troubleshooting

### Common Issues:
1. **API Connection Errors**: Check internet connection and try refreshing
2. **No Data Loading**: The FPL API may be temporarily unavailable
3. **Team Generation Fails**: Try increasing budget or check if gameweek is active

### Performance Notes:
- Initial data load may take 5-10 seconds
- Team generation typically takes 1-3 seconds
- Sorting large player lists may have slight delay

## Future Enhancements

Potential features for future versions:
- Player fixture difficulty analysis
- Injury and suspension tracking
- Price change predictions
- Historical performance graphs
- Transfer suggestions
- Captain recommendations
- Save/load team configurations

## License

This project is for educational and personal use. All FPL data is owned by the Premier League.