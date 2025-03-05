package rules.projects;

public class p1 {
    public static void main(String[] args) {
        String[] words = generateRandomWords(1000, 20);
        int repetitions = 5;

        for (int i = 0; i < repetitions; i++) {
            String result = "";
            for (String word : words) {
                result += word;
            }
        }
    }

    public static String[] generateRandomWords(int numberOfWords, int wordLength) {
        return new String[numberOfWords];
    }
}