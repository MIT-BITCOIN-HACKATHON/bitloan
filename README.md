# BitLoan

A decentralized lending platform built for the MIT Bitcoin Hackathon 2025, leveraging Lightning Network for instant, low-fee transactions.

## 🚀 Overview

BitLoan is a peer-to-peer lending platform that uses the Lightning Network to facilitate instant loans and repayments. The platform consists of three main components:

- **Frontend**: Next.js-based web application
- **Backend**: Python-based API server
- **Lightning Network Integration**: LNbits-based payment processing

## 🛠️ Tech Stack

### Frontend
- Next.js
- TypeScript
- Tailwind CSS
- ESLint

### Backend
- Python
- FastAPI
- LNbits API
- Voltage API

### Lightning Network
- LNbits
- Docker

## 📋 Prerequisites

- Node.js (v18 or higher)
- Python 3.8+
- Docker
- Git

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone [repository-url]
cd bitloan
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 4. Lightning Network Setup
[Instructions for setting up LNbits with Docker will be added]

## 🏗️ Project Structure

```
bitloan/
├── frontend/          # Next.js frontend application
├── backend/           # Python backend server
├── app/              # LNbits integration and demo
│   ├── src/          # Source code
│   └── requirements.txt
└── nodes/            # Lightning Network node configurations
```

## 🔑 Key Features

- Instant peer-to-peer lending
- Lightning Network integration
- Real-time payment processing
- Secure wallet management
- User-friendly interface

## 📚 Documentation

- [Frontend Documentation](frontend/README.md)
- [Backend Documentation](backend/README.md)
- [LNbits Integration](app/README.md)
- [Voltage API Documentation](backend/VOLTAGE_API.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- MIT Bitcoin Hackathon 2025
- LNbits Team
- Voltage API Team
- All contributors and supporters

## 📧 Contact

For questions and support, please open an issue in the repository.