from app import create_app

# small change 11

application = create_app()

if __name__ == '__main__':
    application.run(debug=True)
