# **Conceptions Telegram Bot**

The Conceptions Telegram Bot is designed to provide users with access to a library of books and social media links. Users can explore various book categories, select specific books for downloading, and conveniently access Conceptions' social media profiles.

## **Features**

1. **Start Command**: Initiate a conversation with the bot using the `/start` command. The bot will greet you and present options to navigate to the library or social media links.

2. **Library Command**: Use the `Library` command to explore available book categories. Select a category to view books within that category.

3. **Book Selection**: After choosing a category, select a specific book to download. The bot retrieves book information, including title, category, file size, and provides an option to download the book.

4. **Download Limit**: The bot tracks the number of downloads per user and limits downloads to five per category. Users will be notified if they reach the maximum download limit.

5. **Social Media Links**: Access Conceptions' social media profiles using the `Social Media Links` command. The bot provides quick access to platforms like Facebook, YouTube, Instagram, LinkedIn, and TikTok.

To include information about the `.env` file in your README, you can add a section explaining its purpose and how to set it up. Here's how you can incorporate it into your existing README:

### **Setup**

To run the Conceptions Telegram Bot, follow these steps:

1. **Set up Redis**: Create a Redis server and note down the host, port, and password.

2. **Telegram Bot**: Create a bot on the [Telegram Bot Platform](https://core.telegram.org/bots) and obtain an API token.

3. **Conceptions API**: Obtain an API token for the Conceptions API from the platform administrators.

4. **Server Deployment**: Set up a server to host the bot code using platforms like [Heroku](https://www.heroku.com/) or [Google Cloud Platform](https://cloud.google.com/).

5. **Environment Variables**: Use a `.env` file to manage environment variables. Create a file named `.env` in your project directory and define the necessary variables:

    ```
    TELEGRAM_API=your_telegram_api_token
    ROUTE_API=your_conceptions_api_token
    REDIS_HOST=your_redis_host
    REDIS_PORT=your_redis_port
    REDIS_PASSWORD=your_redis_password
    ```

    Replace `your_telegram_api_token`, `your_conceptions_api_token`, `your_redis_host`, `your_redis_port`, and `your_redis_password` with your actual values.

6. **Install Dependencies**: Run `pip install -r requirements.txt` to install the necessary Python packages.

7. **Start the Bot**: Run `python app.py` to start the bot.

## **Usage**

Follow these steps to interact with the Conceptions Telegram Bot:

1. Start a conversation with the bot by searching for its username or clicking on a provided link.

2. Upon starting, the bot will greet you and present options to navigate to the library or social media links.

3. To explore the library, select the `Library` option. Choose a category of interest to view available books.

4. Select a specific book to view details and download options. You can download up to five books per category.

5. Use the `Social Media Links` option to access Conceptions' social media profiles. Click on the provided buttons to open the respective links.

## **About**

The Conceptions Telegram Bot was developed by Sai Khant Zay Lynn Yaung to provide users with easy access to a library of books and Conceptions' social media profiles.

For more information, contact Sai Khant Zay Lynn Yaung at khantzay.ly@gmail.com.

Thank you for using the Conceptions Telegram Bot! We hope you enjoy your reading experience and find the social media links helpful.