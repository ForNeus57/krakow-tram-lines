from ktl.model.people import *

def main() -> None:
    people = generate_people(0.5, range(100))
    for person in people:
        print(person.name)


if __name__ == "__main__":
    main()
