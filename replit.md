# Overview

This is a comprehensive blockchain analytics dashboard that provides real-time cryptocurrency market data, AI-powered price predictions, and technical pattern analysis. The application serves as a centralized platform for monitoring cryptocurrency markets with advanced analytics capabilities including machine learning predictions, technical indicator analysis, and DeFi protocol monitoring.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Technology Stack**: Bootstrap 5 with dark theme, Chart.js for data visualization, Font Awesome icons
- **Template Engine**: Jinja2 templates with Flask
- **Responsive Design**: Mobile-first Bootstrap grid system with custom CSS enhancements
- **Real-time Updates**: JavaScript-based auto-refresh functionality with caching mechanisms
- **Visualization**: Interactive charts for price data, predictions, and pattern analysis

## Backend Architecture
- **Framework**: Flask web framework with modular route organization
- **Service Layer**: Separated business logic into dedicated service classes
- **API Design**: RESTful endpoints for market data, predictions, and pattern analysis
- **Error Handling**: Comprehensive logging and exception handling throughout the application
- **Caching**: In-memory caching for API responses to reduce external service calls

## Data Processing & Analytics
- **Machine Learning**: scikit-learn based prediction models including Random Forest and Linear Regression
- **Technical Analysis**: Custom pattern recognition algorithms for support/resistance, trend analysis, and momentum indicators
- **Feature Engineering**: Automated creation of technical indicators (RSI, moving averages, volatility measures)
- **Data Pipeline**: Pandas-based data processing with timestamp handling and feature lag creation

## Authentication & Security
- **Session Management**: Flask session handling with configurable secret keys
- **Environment Variables**: Secure configuration management for sensitive data
- **Input Validation**: Request parameter validation and sanitization
- **CORS Handling**: Proper cross-origin request handling for API endpoints

# External Dependencies

## Cryptocurrency Data API
- **Primary Service**: CoinGecko API for real-time market data, historical prices, and volume information
- **Rate Limiting**: Built-in request throttling and caching to respect API limits
- **Data Coverage**: Support for top cryptocurrencies, market statistics, and DeFi protocols

## Machine Learning Libraries
- **scikit-learn**: Core ML algorithms for price prediction models
- **pandas**: Data manipulation and analysis framework
- **numpy**: Numerical computing for statistical calculations
- **scipy**: Statistical analysis and signal processing for pattern detection

## Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme optimization
- **Chart.js**: Interactive charting library for price and prediction visualizations
- **Font Awesome**: Icon library for consistent UI elements

## Development & Deployment
- **Flask**: Web framework for API and template rendering
- **Gunicorn**: WSGI HTTP server for production deployment (implied)
- **Environment Configuration**: Support for development and production configurations

## Data Storage Considerations
- **Current State**: In-memory caching and processing
- **Future Extension**: Architecture supports addition of persistent database layer for historical data storage and user preferences