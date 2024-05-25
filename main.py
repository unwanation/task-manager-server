import uvicorn

import db.schemas


def main():
    db.create_db()
    uvicorn.run(
        "app:app",
        reload=True,
    )


if __name__ == "__main__":
    main()
