import uvicorn
from circlepacker import service


def main(port: int = 5001) -> None:

    uvicorn.run(service.app, port=port)


if __name__ == "__main__":
    main()
