compile: node_modules
node_modules: package.json
	npm install
	touch node_modules
serve: compile
	npm start

package: compile
	npm run build
clean:
	rm -rf build
	rm -rf node_modules
