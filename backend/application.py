from app import create_app

# small change 14

application = create_app()

if __name__ == '__main__':
    application.run(debug=True)
