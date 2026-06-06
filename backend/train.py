from model import train
from preprocessing import load_training_data

FILE_PATH = "../data/raw/nsl-kdd/KDDTrain+.csv"

def main():
    df = load_training_data(FILE_PATH)
    train(df)


if __name__ == "__main__":
    main()