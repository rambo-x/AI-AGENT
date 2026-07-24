module.exports = {
  apps: [
    {
      name: "tripleside-ai-agent",
      script: "app.py",
      interpreter: "/home/triplesidestudio/tripleside-ai-agent/venv/bin/python",
      cwd: "/home/triplesidestudio/tripleside-ai-agent",
      autorestart: true,
      watch: false,
      max_memory_restart: "200M",
      env: {
        NODE_ENV: "production"
      }
    }
  ]
}
