import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:pdf_text/pdf_text.dart';

void main() {
  runApp(PdfToAudioApp());
}

class PdfToAudioApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'PDF to Audiobook',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: PdfToSpeechScreen(),
    );
  }
}

class PdfToSpeechScreen extends StatefulWidget {
  @override
  _PdfToSpeechScreenState createState() => _PdfToSpeechScreenState();
}

class _PdfToSpeechScreenState extends State<PdfToSpeechScreen> {
  FlutterTts flutterTts = FlutterTts();
  String extractedText = "";
  bool isPlaying = false;

  Future<void> pickAndReadPdf() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result != null) {
      File file = File(result.files.single.path!);
      PDFDoc pdfDoc = await PDFDoc.fromFile(file);
      String text = await pdfDoc.text; // Extract text from PDF

      setState(() {
        extractedText = text;
      });
    }
  }

  Future<void> speakText() async {
    if (extractedText.isNotEmpty) {
      await flutterTts.speak(extractedText);
      setState(() => isPlaying = true);
    }
  }

  Future<void> stopSpeech() async {
    await flutterTts.stop();
    setState(() => isPlaying = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('PDF to Audiobook')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            ElevatedButton(
              onPressed: pickAndReadPdf,
              child: Text("Select PDF"),
            ),
            SizedBox(height: 20),
            Expanded(
              child: SingleChildScrollView(
                child: Text(extractedText, style: TextStyle(fontSize: 16)),
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: isPlaying ? stopSpeech : speakText,
              child: Text(isPlaying ? "Stop" : "Play"),
            ),
          ],
        ),
      ),
    );
  }
}
