# API for a database

## GET
`/users` - returns all users
`/user/(id)` - returns a user with that id

## POST
`/users/` - adds a new user
### Body:
```json
{
    "name": "name"
}
```

## PUT
`/user/(id)` - updates the user with that id
### Body:
```json
{
    "name": "name"
}
```

## DELETE
`/user/(id)` - deletes the user with that id
