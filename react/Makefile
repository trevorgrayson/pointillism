serve: compile
	npm start

compile: node_modules
node_modules: package.json
	npm install
	touch node_modules

package: compile
	npm run build
	rm -rf ../point/server/static/static
	cp -rf build/* ../point/server/static/
	cp ../point/server/static/favicon.ico ../point/server/static/static/
	cp ../point/server/static/robots.txt ../point/server/static/static/
	cp build/privacy.html ../point/server/static/privacy.html
	cp build/index.html ../public/index.html


clean:
	rm -rf build
	rm -rf node_modules
