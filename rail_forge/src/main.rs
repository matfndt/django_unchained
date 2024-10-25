use dotenv::dotenv;
use std::env;

#[tokio::main]
async fn main() {
    dotenv().ok(); // load env file for database
    let db_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
}
