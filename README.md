# cleanArchitectureBaseExample
Use vscode Debugger -> launch.json
Replace .env file with .env.production.example or .env.test.example depend your enviroment
### Test
    Run "Docker: Run Test"
 
### Development && Production
    Run "Docker: Build Web" # Only fist time
    Run "Docker: Run Application" 
    Run "Postgres: Init DB"

#####  Only first time or during migrations update
In external Debugger Terminal
    ```sh
        direnv allow .
    ```
    ```sh
        alembic revision --autogenerate -m "Initial"
    ```
    ```sh
        alembic upgrade head 
    ```
