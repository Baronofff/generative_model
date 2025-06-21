"""
Generation by NGrams starter
"""
from main import (BeamSearchTextGenerator, GreedyTextGenerator,
                  NGramLanguageModel, TextProcessor, BackOffGenerator)


def main() -> None:
    """
    Launches an implementation.

    In any case returns, None is returned
    """
    with open(r"C:\Users\user\programming_projects\generative_model\texts\collect_mini.txt",
              "r", encoding="utf-8") as text_file:
        text = text_file.read()
    processor = TextProcessor(end_of_word_token='_')
    encoded = processor.encode(text)
    if not (isinstance(encoded, tuple) and encoded):
        return

    decoded = str(processor.decode(encoded))
    result = decoded

    model_10 = NGramLanguageModel(encoded, 10)

    model_7 = NGramLanguageModel(encoded, 7)

    model_5 = NGramLanguageModel(encoded, 5)

    print("Model 10 built successfully?", model_10.build() == 0)  # Должно быть True
    print("Model 7 built successfully?", model_7.build() == 0)  # Должно быть True
    print("Model 5 built successfully?", model_5.build() == 0)  # Должно быть True

    print('\n')

    print("Number of 10-grams:", len(model_10._n_gram_frequencies))
    print("Number of 7-grams:", len(model_7._n_gram_frequencies))
    print("Number of 5-grams:", len(model_5._n_gram_frequencies))

    print('\n')

    print("greedy_text_generator:")
    greedy_text_generator = GreedyTextGenerator(model_10, processor)
    print(greedy_text_generator.run(50, 'Он понимал, что'))
    print(greedy_text_generator.run(50, 'с большою радостью готов был отправить'))

    print('\n')

    print("beam_search_generator:")
    beam_search_generator = BeamSearchTextGenerator(model_7, processor, 10)
    print(beam_search_generator.run('Он понимал, что', 50))
    print(beam_search_generator.run('Он корточки приподня с', 50))

    print('\n')

    print("back_off_generator:")
    back_off_generator = BackOffGenerator(
        language_models=(model_10,
                         model_7,
                         model_5), text_processor=processor)
    print(back_off_generator.run(prompt='Он понимал, что', seq_len=50))
    print(back_off_generator.run(prompt='Он корточки приподня с', seq_len=50))

    assert result


if __name__ == "__main__":
    main()
