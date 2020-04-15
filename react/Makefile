serve: compile
	npm start

compile: node_modules
node_modules: package.json
	npm install
	touch node_modules

package: compile
	npm run build
	cp -rf build/* ../server/static/

clean:
	rm -rf build
	rm -rf node_modules
