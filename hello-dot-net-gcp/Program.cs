
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorPages();

builder.Services.AddHttpClient(); 

var app = builder.Build();

app.UseStaticFiles(); // Good practice for CSS/JS
app.UseRouting();    

app.MapGet("/hello", () => "<title>Hello World </title> <h1>Hello World from Azure first then GKE!</h1>");

app.MapRazorPages();

app.Run();
