async def hello(ctx, DELETE_MESSAGE_TIME):
    await ctx.send("Hello! I'm your bot.", delete_after=DELETE_MESSAGE_TIME)

async def ping(ctx, bot, DELETE_MESSAGE_TIME):
    latency = bot.latency * 1000  # Convert to milliseconds
    await ctx.send(f"Pong! Latency: {latency:.2f} ms", delete_after=DELETE_MESSAGE_TIME)

async def health_cmd(ctx, bot, DELETE_MESSAGE_TIME):
    # Delete the command message
    await ctx.message.delete()

    message = await ctx.send("I'm alive and kicking!", delete_after=DELETE_MESSAGE_TIME)
    latency = bot.latency * 1000
    await message.edit(content=f"I'm alive and kicking! Latency: {latency:.2f} ms", delete_after=DELETE_MESSAGE_TIME)
