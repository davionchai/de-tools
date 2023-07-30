.PHONY: get-ip clean

get-ip:
	ipconfig getifaddr en0

clean:
	@rm -rf logs
	@find . -type d -name "__pycache__" -exec rm -rf {} +
