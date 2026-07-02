using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// ❌ DE01 baseline: no compression middleware. Participants add:
// builder.Services.AddResponseCompression();

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();
// app.UseResponseCompression();

var items = Enumerable.Range(1, 200).Select(i => new Dictionary<string, object>
{
    ["id"] = i,
    ["title"] = $"Item #{i}",
    ["description"] = string.Concat(Enumerable.Repeat("Long description body ", 20)),
    ["updatedAt"] = DateTimeOffset.UtcNow.ToString("O"),
}).ToList();

app.MapGet("/health", () => Results.Ok(new { status = "UP" }));

// ❌ DE11: no pagination.
app.MapGet("/items", () => Results.Ok(items));

// ❌ DE02/03: no ETag.
app.MapGet("/items/{id:int}", (int id) =>
    items.FirstOrDefault(x => (int)x["id"] == id) is { } item ? Results.Ok(item) : Results.NotFound());

// ❌ AR01: polling-style. Should become SSE.
app.MapGet("/items/events", () => Results.Ok(items.Take(5)));

// ✅ DE06 baseline.
app.MapGet("/items/changes", ([FromQuery] long? since) => Results.Ok(items.Take(3)));

app.MapPost("/items", ([FromBody] Dictionary<string, object> body) =>
{
    body["id"] = items.Count + 1;
    return Results.Ok(body);
});

app.Run();

