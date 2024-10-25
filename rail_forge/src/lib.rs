use serde::{Deserialize, Serialize};
use sqlx::query_as;
use std::collections::HashMap;

#[derive(Serialize, Deserialize)]
pub struct User {
    pub id: i32,
    pub name: String,
    pub age: i32,
    pub region: String,
}

pub async fn fetch_records(
    model: &str,
    filters: HashMap<String, serde_json::Value>,
    excludes: HashMap<String, serde_json::Value>,
    ordering: Vec<String>,
    annotations: HashMap<String, String>,
) -> Result<Vec<User>, sqlx::Error> {
    // generate the sql
    let sql_query = format!("SELECT * FROM {} WHERE ...", model);

    // how to handle types?
    // through trait?
    // let result = query_as!(User, &sql_query).fetch_all(&pool).await?;

    Ok(result)
}
