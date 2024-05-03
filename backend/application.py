from app import create_app

# small change 9

application = create_app()

if __name__ == '__main__':
    application.run(debug=True)
