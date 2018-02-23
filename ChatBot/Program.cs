using System;
using System.Threading.Tasks;
using System.Reflection;
using Discord;
using Discord.WebSocket;
using Discord.Commands;
using Microsoft.Extensions.DependencyInjection;
using System.IO;
using System.Linq;

namespace ChatBot
{
    class Program
    {
        //public string token = "Mzg2NDgwNjMwOTUyNjI0MTI5.DQQigw.dJCaz4Q7eMyHgy2CPFfXFODdzS4";
        public Random rnd = new Random();
        public char prefix = ';';

        public void Setup()
        {

            AppDomain.CurrentDomain.AssemblyResolve += (sender, args) =>
            {

                Assembly thisAssembly = Assembly.GetExecutingAssembly();

                //Get the Name of the AssemblyFile
                var name = args.Name.Substring(0, args.Name.IndexOf(',')) + ".dll";

                //Load form Embedded Resources - This Function is not called if the Assembly is in the Application Folder
                var resources = thisAssembly.GetManifestResourceNames().Where(s => s.EndsWith(name));
                if (resources.Count() > 0)
                {
                    var resourceName = resources.First();
                    using (Stream stream = thisAssembly.GetManifestResourceStream(resourceName))
                    {
                        if (stream == null) return null;
                        var block = new byte[stream.Length];
                        stream.Read(block, 0, block.Length);
                        return Assembly.Load(block);
                    }
                }
                return null;
            };
        }

        private CommandService commands;
        private DiscordSocketClient client;
        private IServiceProvider services;

        static void Main(string[] args) => new Program().Start().GetAwaiter().GetResult();

        public async Task Start()
        {
            //Set up console colours
            Console.ForegroundColor = ConsoleColor.White;
            Console.BackgroundColor = ConsoleColor.Black;

            Console.WriteLine("===  Initializing ChatBot   ===");
            ConsoleLog("Starting process...");
            Setup();
            ConsoleLog("Setup complete!");

            //Get the token for the bot from a file
            StreamReader file = new StreamReader(Environment.CurrentDirectory + "\\Token.txt");
            string token = file.ReadLine();

            ConsoleLog("Sucessfully got token from file");

            client = new DiscordSocketClient(new DiscordSocketConfig
            {
                WebSocketProvider = Discord.Net.Providers.WS4Net.WS4NetProvider.Instance,
                LogLevel = LogSeverity.Info
            });

            ConsoleLog("Client set up");

            commands = new CommandService();
            ConsoleLog("Set commands as new CommandService");

            services = new ServiceCollection()
                    .BuildServiceProvider();

            ConsoleLog("Set services as new ServiceCollection");

            await InstallCommands();
            ConsoleLog("Installed Commands");

            client.Log += Log;

            await client.LoginAsync(TokenType.Bot, token);
            await client.StartAsync();

            ConsoleLog("Establishing connection...");

            await Task.Delay(-1);
        }
        private Task Log(LogMessage message)
        {
            var cc = Console.ForegroundColor;
            switch (message.Severity)
            {
                case LogSeverity.Critical:
                case LogSeverity.Error:
                    Console.ForegroundColor = ConsoleColor.Red;
                    break;
                case LogSeverity.Warning:
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    break;
                case LogSeverity.Info:
                    Console.ForegroundColor = ConsoleColor.White;
                    break;
                case LogSeverity.Verbose:
                case LogSeverity.Debug:
                    Console.ForegroundColor = ConsoleColor.White;
                    break;
            }
            ConsoleLog(message.Message);
            Console.ForegroundColor = cc;

            return Task.CompletedTask;
        }
        public async Task InstallCommands()
        {
            // Hook the MessageReceived Event into our Command Handler
            client.MessageReceived += HandleCommand;
            // Discover all of the commands in this assembly and load them.
            await commands.AddModulesAsync(Assembly.GetEntryAssembly());
        }
        public async Task HandleCommand(SocketMessage messageParam)
        {
            // Don't process the command if it was a System Message
            var msg = messageParam as SocketUserMessage;
            if (msg == null) return;
            // Create a number to track where the prefix ends and the command begins
            int pos = 0;
            IServiceProvider service = null;
            // Determine if the message is a command, based on if it starts with the prefix character or a mention prefix
            //ConsoleLog("Message content 1st char is: " + msg.Content.ToString().Substring(0, 1));

            string firstChar = msg.Content.ToString().Substring(0, 1);
            char firstChar1 = Char.Parse(firstChar);

            if (firstChar1.Equals(prefix))
            {
                ConsoleLog("Message is a command");

                //Ping
                if (messageParam.Content.Equals(prefix + "ping"))
                {
                    ConsoleLog("Running ping command...");
                    await msg.Channel.SendMessageAsync(Commands.Ping());
                }

                //Wednesday
                if (messageParam.Content.Equals(prefix + "wednesday"))
                {
                    ConsoleLog("Running wednesday command...");
                    await msg.Channel.SendMessageAsync(Commands.Wednesday());
                }

                //ToggleReplies
                if (messageParam.Content.Equals(prefix + "togglereplies"))
                {
                    ConsoleLog("Toggling replies...");
                    await msg.Channel.SendMessageAsync(Commands.ToggleReplies());
                }

                /*
                                
                // Create a Command Context
                var context = new CommandContext(client, msg);
                IServiceProvider service = null;
                // Execute the command. (result does not indicate a return value, rather an object stating if the command executed successfully)
                var result = await commands.ExecuteAsync(context, pos, service);
                if (!result.IsSuccess)
                    await context.Channel.SendMessageAsync(result.ErrorReason);
            
                */

            }
            else if (msg.Author.Username.Equals("ChatBot"))
            {
                return;
            }
            else
            {

                if (Commands.RandomReplyToggle == true)
                {

                    int decider = rnd.Next(1, 10);
                    if (decider == 5)
                    {
                        ConsoleLog("Message recieved, will be replied to");

                        await msg.Channel.SendMessageAsync(RandomResponse.GetRandomReply() + MentionUtils.MentionUser(msg.Author.Id));
                        return;
                    }
                    else
                    {
                        ConsoleLog("Message recieved, will not be replied to");
                        return;
                    }
                }
            }


        }
        public void ConsoleLog(string message)
        {
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine(DateTime.Now.TimeOfDay.Hours.ToString("00") + ":" + DateTime.Now.TimeOfDay.Minutes.ToString("00") + ":" + DateTime.Now.TimeOfDay.Seconds.ToString("00") + " " + "{0}", message);
        }

    }
    class Commands
    {
        public static bool RandomReplyToggle = false;

        internal static bool GetReplies()
        {
            return RandomReplyToggle;
        }

        internal static string ToggleReplies()
        {
            {
                if (RandomReplyToggle == false)
                {
                    RandomReplyToggle = true;
                    return "Random replies turned on";
                }
                else
                {
                    RandomReplyToggle = false;
                    return "Random replies turned off";
                }
            }
        }

        internal static string Ping()
        {
            return "Pong!";
        }

        internal static string Wednesday()
        {

            if (DayOfWeek.Wednesday == DateTime.Now.DayOfWeek)
            {
                return "It is wednesday, my dudes. https://i.imgur.com/SPDD3R2.jpg";
            }
            else
            {
                return "It is NOT wednesday, my dudes";
            }
        }


    }
    class RandomResponse
    {

        internal static string GetRandomReply()
        {
            Random rnd = new Random();
            int response = rnd.Next(1, 10);

            switch (response)
            {
                case 1:
                    return "rhodso hates you, ";
                case 2:
                    return "Fuck off, ";
                case 3:
                    return "Kill yourself, ";
                case 4:
                    return "You're a cunt, ";
                case 5:
                    return "You're not that bad, ";
                case 6:
                    return "Why are you still here? Don't you understand that nobody actually wants you here, ";
                default:
                    return "Fuck you, ";

            }
        }
    }
}
