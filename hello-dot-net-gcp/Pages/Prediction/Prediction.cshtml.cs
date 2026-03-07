using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Text;
using System.Text.Json;

namespace YourAppName.Pages.Prediction
{
    public class PredictionModel : PageModel
    {
        private readonly IHttpClientFactory _clientFactory;
        private readonly IConfiguration _config;

        public PredictionModel(IHttpClientFactory clientFactory, IConfiguration config)
        {
            _clientFactory = clientFactory;
            _config = config;
        }

        [BindProperty]
        public TenantInputFormData TenantData { get; set; } = new TenantInputFormData();

        public string? PredictionResult { get; set; }
        public double? RiskProbability { get; set; }
        public string? ErrorMessage { get; set; }

        public void OnGet()
        {
            // Page load - nothing to do here yet
        }

        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid)
            {
                return Page();
            }

            // Read the environment variables injected by Kubernetes
            var apiUrl = _config.GetValue<string>("PYTHON_API_URL") ?? "http://python-api-internal/predict";
            var apiKey = _config.GetValue<string>("API_KEY") ?? "dev-secret-key-123";

            var client = _clientFactory.CreateClient();
            
            // Serialize the form data to JSON
            var jsonContent = new StringContent(
                JsonSerializer.Serialize(TenantData), 
                Encoding.UTF8, 
                "application/json"
            );

            // Create the request and attach the required API Key header
            var request = new HttpRequestMessage(HttpMethod.Post, apiUrl)
            {
                Content = jsonContent
            };
            request.Headers.Add("x-api-key", apiKey);

            try
            {
                var response = await client.SendAsync(request);
                
                if (response.IsSuccessStatusCode)
                {
                    var responseStream = await response.Content.ReadAsStreamAsync();
                    var result = await JsonSerializer.DeserializeAsync<PredictionResponse>(responseStream);
                    
                    // Maps to Class 0 or Class 1
                    PredictionResult = result?.prediction_class; 
                    RiskProbability = result?.risk_probability;
                }
                else
                {
                    ErrorMessage = $"API Error: {response.StatusCode}. Please ensure the Python API pod is running.";
                }
            }
            catch (Exception ex)
            {
                ErrorMessage = $"Connection Error: {ex.Message}. Check the Kubernetes ClusterIP service routing.";
            }

            return Page();
        }
    }

    // Data structure matching the Random Forest inputs
    public class TenantInputFormData
    {
        public double monthly_income { get; set; }
        public double monthly_debt { get; set; }
        public int employment_tenure_months { get; set; }
        public double years_at_prev_address { get; set; }
        public int prev_evictions { get; set; } // 0 or 1
        public int late_payment_count { get; set; }
        public int credit_score { get; set; }
        public double proposed_rent { get; set; }
    }

    // Data structure matching the Python API output
    public class PredictionResponse
    {
        public string? prediction_class { get; set; }
        public double risk_probability { get; set; }
    }
}