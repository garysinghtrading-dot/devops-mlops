FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Use the EXACT name of the file you saw earlier
COPY helloDotNet.csproj .
RUN dotnet restore

COPY . .
RUN dotnet publish -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .

# THIS IS THE MOST CRITICAL LINE - MUST BE EXACT CASE
ENTRYPOINT ["dotnet", "helloDotNet.dll"]