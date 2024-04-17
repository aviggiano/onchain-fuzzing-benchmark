const fs = require('fs')
console.log('name,seq,date,time,cov,corpus,fuzzing')
for (let i = 0; i <= 9; i++) {
	const l = fs.readFileSync(`/tmp/local-${i}.txt`, 'utf8')
	const r = fs.readFileSync(`/tmp/remote-${i}.txt`, 'utf8')
	const files = [
		{ name: 'local', content: l },
		{ name: 'remote', content: r }
	]
	for (const file of files) {
		const lines = file.content.split('\n')
		let isFirst = true
		let t0
		for (const line of lines) {
			// [2024-04-16 18:08:24.38] [status] tests: 0/1, fuzzing: 0/1000000, values: [0], cov: 3063, corpus: 0
			const isMatch = line.match(/.*\[status\].*/)
			if (!isMatch) continue

			const date = line.match(/\[(.*?)\]/)[1]
			let time = new Date(date).getTime()
			if (isFirst) {
				t0 = time
				isFirst = false
			}
			time = time - t0

			const cov = line.match(/cov: (\d+)/)[1]
			const corpus = line.match(/corpus: (\d+)/)[1]
			const fuzzing = line.match(/fuzzing: (\d+)/)[1]
			console.log([
				file.name,
				i,
				date,
				time,
				cov,
				corpus,
				fuzzing
			].join(','))
		}
	}
}