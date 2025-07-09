.PHONY: test build deploy all

# Run tests
test:
	@echo "Running tests..."
	pytest
	@echo "Tests passed!"

# Build MkDocs site
build: test
	@echo "Building documentation..."
	mkdocs build

# Deploy to GitHub Pages
deploy: build
	@echo "Deploying to GitHub Pages..."
	mkdocs gh-deploy --clean

# Do everything
all: deploy
