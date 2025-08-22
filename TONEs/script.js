let synths = [];
let loops = [];

function clearAudio() {
  loops.forEach(l => Tone.Transport.clear(l));
  loops = [];
  synths.forEach(s => s.dispose());
  synths = [];
}

function stopMusic() {
  Tone.Transport.stop();
  clearAudio();
  console.log('🛑 Музыка остановлена');
}

async function startMonetLoop() {
  await Tone.start();
  stopMusic();

  // Мягкий синт
  const synth = new Tone.PolySynth(Tone.Synth, {
    oscillator: { type: "triangle" },
    envelope: {
      attack: 0.1,
      decay: 0.2,
      sustain: 0.4,
      release: 1.2
    }
  });

  synth.volume.value = -8;

  // Эффекты
  const chorus = new Tone.Chorus(4, 2.5, 0.5).start();
  const reverb = new Tone.Reverb(2).toDestination();

  synth.connect(chorus);
  chorus.connect(reverb);

  synths.push(synth, chorus, reverb);

  // Настройка темпа
  Tone.Transport.bpm.value = 250;

  // F#m – A – C# – A – F#m – D# – F#m – C#
  const chords = [
    ["F#3", "A3", "C#4"],
    ["A3", "C#4", "E4"],
    ["C#3", "E3", "G#3"],
    ["A3", "C#4", "E4"],
    ["F#3", "A3", "C#4"],
    ["D#3", "F3", "A#3"],
    ["F#3", "A3", "C#4"],
    ["C#3", "E3", "G#3"]
  ];

  let i = 0;

  loops.push(
    Tone.Transport.scheduleRepeat(time => {
      synth.triggerAttackRelease(chords[i % chords.length], "2n", time);
      i++;
    }, "2n")
  );

  // Бит
  const kick = new Tone.MembraneSynth().toDestination();
  const clap = new Tone.NoiseSynth({
    noise: { type: "white" },
    envelope: { attack: 0.005, decay: 0.1, sustain: 0 }
  }).toDestination();

  loops.push(
    Tone.Transport.scheduleRepeat(time => {
      kick.triggerAttackRelease("C1", "8n", time);
    }, "1n")
  );

  loops.push(
    Tone.Transport.scheduleRepeat(time => {
      clap.triggerAttackRelease("8n", time + 0.5);
    }, "1n")
  );

  Tone.Transport.start();
}
