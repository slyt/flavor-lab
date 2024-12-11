
import json
import logging
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Load flavor wheel data from JSON file
def load_flavor_wheel():
    with open("flavor_wheel.json", "r") as f:
        return json.load(f)

flavor_wheel_data = load_flavor_wheel()

# Define the GraphQL schema
@strawberry.type
class Category:
    name: str
    similar_ingredients: list[str]

@strawberry.type
class FlavorWheel:
    core_ingredient: str
    categories: list[Category]

@strawberry.type
class Query:
    @strawberry.field
    def get_flavor_wheel(self, ingredient: str) -> FlavorWheel:
        if ingredient.lower() == flavor_wheel_data["core_ingredient"].lower():
            categories = [
                Category(name=category, similar_ingredients=data["similar_ingredients"])
                for category, data in flavor_wheel_data["categories"].items()
            ]
            return FlavorWheel(core_ingredient=ingredient, categories=categories)
        else:
            raise ValueError(f"No data found for ingredient: {ingredient}")

schema = strawberry.Schema(query=Query)

# FastAPI setup
app = FastAPI()


# Mount the directory where index.html and other static files are located
app.mount("/static", StaticFiles(directory="."), name="static")

# Serve index.html when accessing the root URL
@app.get("/")
async def read_index():
    return FileResponse("index.html")

# GraphQL route
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Root endpoint for testing
@app.get("/")
async def read_root():
    return {"message": "Hello, GraphQL is now integrated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
