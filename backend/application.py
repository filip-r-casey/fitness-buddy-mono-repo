from app import create_app

# small change 8

application = create_app()

if __name__ == '__main__':
    application.run(debug=True)
