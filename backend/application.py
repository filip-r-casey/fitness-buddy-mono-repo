from app import create_app

# small change

application = create_app()

if __name__ == '__main__':
    application.run(debug=True)
